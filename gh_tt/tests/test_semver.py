import string
from enum import Enum, auto

import pytest
from hypothesis import given
from hypothesis import strategies as st

from gh_tt.classes.gitter import Gitter
from gh_tt.classes.semver import ExecutionMode, ReleaseType, Semver, SemverVersion
from gh_tt.tests.testbed import Testbed


@pytest.mark.unittest
def test_semver_init(capsys):
    Gitter.verbose = False

    semver = Semver()
    assert isinstance(semver, Semver)
    assert semver.get("initial") == "0.0.0"
    semver = None

    # No longer supporting suffix parameter
    semver = Semver(prefix="v", initial="1.4.1")
    assert isinstance(semver, Semver)
    assert semver.get("initial") == "1.4.1"
    # No suffix property anymore
    assert semver.get("prefix") == "v"

    semver = None

    with pytest.raises(SystemExit) as cm:
        semver = Semver(initial="bad.initial.3")

    assert cm.value.code == 1
    assert "Invalid initial version" in capsys.readouterr().err


@pytest.mark.unittest
def test_semver_list(capsys):
    # Setup
    semver = Semver().from_json("gh_tt/tests/data/semver/semver_loaded_release_and_prerelease.json")
    semver.set('semver_tags', semver._parse_tags(semver.get('tags'), prefix=None))

    assert isinstance(semver, Semver)

    semver.list(release_type=ReleaseType.PRERELEASE)
    output = capsys.readouterr().out

    assert "1.0.1-rc1\n" in output
    assert "1.0.11-rc1\n" in output

    semver.list(release_type=ReleaseType.RELEASE)
    output = capsys.readouterr().out
    assert "0.7.3\n" in output
    assert "0.6.1\n" in output

@pytest.mark.unittest
def test_semver_get_current():
    semver = Semver().from_json('gh_tt/tests/data/semver/semver_loaded_release_and_prerelease.json')
    semver.set('semver_tags', semver._parse_tags(semver.get('tags'), prefix=None))

    release = semver.get_current_semver()
    assert str(release) == "0.7.3"

    prerelease = semver.get_current_semver(release_type=ReleaseType.PRERELEASE)
    assert str(prerelease) == "1.0.11-rc1"

@pytest.mark.unittest
def test_semver_bump(capsys):
    semver = Semver().from_json('gh_tt/tests/data/semver/semver_loaded_release_and_prerelease.json')
    semver.set('semver_tags', semver._parse_tags(semver.get('tags'), prefix=semver.get('prefix')))

    semver.bump("patch", message="Test patch bump", release_type=ReleaseType.PRERELEASE, execution_mode=ExecutionMode.DRY_RUN)
    output = capsys.readouterr().out
    assert "git tag -a -m \"1.0.12-alpha1" in output  # Check the prefix part
    assert "Bumped patch from version '1.0.11-rc1' to '1.0.12-alpha1" in output
    assert "Test patch bump\"" in output


@pytest.mark.unittest
def test_semver_first_prerelease(capsys):
    # Setup
    semver = Semver().from_json("gh_tt/tests/data/semver/semver_loaded_release.json")
    semver.set('semver_tags', semver._parse_tags(semver.get('tags'), prefix=semver.get('prefix')))

    assert isinstance(semver, Semver)

    semver.list(release_type=ReleaseType.PRERELEASE)
    assert capsys.readouterr().out == ""

    semver.list(release_type=ReleaseType.RELEASE)
    output = capsys.readouterr().out
    assert "0.7.3\n" in output
    assert "0.6.1\n" in output

    release = semver.get_current_semver()
    assert str(release) == "0.7.3"

    prerelease = semver.get_current_semver(release_type=ReleaseType.PRERELEASE)
    assert prerelease is None


@pytest.mark.unittest
def test_semver_first_prerelease_bump(capsys):
    semver = Semver().from_json('gh_tt/tests/data/semver/semver_loaded_release.json')
    semver.set('semver_tags', semver._parse_tags(semver.get('tags'), prefix=semver.get('prefix')))

    semver.bump("patch", message="Test patch bump", release_type=ReleaseType.PRERELEASE, execution_mode=ExecutionMode.DRY_RUN)
    output = capsys.readouterr().out
    assert "git tag -a -m \"0.7.4-alpha1" in output
    assert "Bumped patch from version '0.7.3' to '0.7.4-alpha1'" in output
    assert "Test patch bump\"" in output

@pytest.mark.integration
def test_note_with_one_release():
    [extension_list, _] = Testbed.gitter_run(cmd='gh extension list')
    if 'thetechcollective/gh-tt' in extension_list:
        raise SystemExit(
            "You have a remote version of the 'gh-tt' extension installed.\n"
            "Your local changes would not be taken into consideration when running the integration test.\n"
            "Remove the existing extension with `gh extension remove gh-tt`, then \n"
            "install the local version with `gh extension install .`"
        )

    with Testbed.create_local_repo() as repo:
        (repo / 'file1.txt').write_text('text')
        Testbed.gitter_run_all(['git add .', 'git commit -m "file1"'], cwd=repo)
        (repo / 'file2.txt').write_text('text')
        Testbed.gitter_run_all(['git add .', 'git commit -m "file2"', 'git tag 1.0.0', 'gh tt semver note --filename note.md'], cwd=repo)

        assert (repo / 'note.md').read_text().find('Release Notes') != -1

@st.composite
def semver_versions(draw, *, with_prerelease: bool = False, prerelease_id: str | None = None) -> SemverVersion:
    # If prerelease_id is provided, use it; otherwise generate random one
    prerelease_value = None
    if with_prerelease:
        if prerelease_id is not None:
            identifier = prerelease_id
        else:
            identifier = draw(st.text(alphabet=list(string.ascii_lowercase), min_size=1, max_size=15))
        
        # Create a prerelease string like "rc1" (no dot)
        prerelease_value = f"{identifier}{draw(st.integers(min_value=1))}"
    
    return SemverVersion(
        major=draw(st.integers(min_value=0)),
        minor=draw(st.integers(min_value=0)),
        patch=draw(st.integers(min_value=0)),
        prerelease=prerelease_value,
        build=None,
    )

class PrereleaseStrategy(Enum):
    MIXED = auto()
    CONSISTENT = auto()


@st.composite
def tag_strings(draw, *, prerelease_strategy: PrereleaseStrategy = PrereleaseStrategy.MIXED) -> str:
    if prerelease_strategy is PrereleaseStrategy.CONSISTENT:
        # Generate a shared prerelease identifier for all prereleases
        shared_id = draw(st.text(alphabet=list(string.ascii_lowercase), min_size=1, max_size=15))
        valid_versions = draw(
            st.lists(
                st.one_of(
                    semver_versions(with_prerelease=False),
                    semver_versions(with_prerelease=True, prerelease_id=shared_id),
                )
            )
        )
    else:  # Prerelease identifier is randomly generated for each SemverVersion
        valid_versions = draw(st.lists(semver_versions(with_prerelease=draw(st.booleans()))))

    other_tags = draw(
        st.lists(
            st.text(alphabet=list(string.ascii_lowercase), min_size=1, max_size=15).filter(
                lambda x: "\n" not in x
            ),
        )
    )

    valid_version_strings = [str(version) for version in valid_versions]
    all_tags = valid_version_strings + other_tags

    draw(st.randoms()).shuffle(all_tags)
    return "\n".join(all_tags)

@given(version=semver_versions())
def test_semver_version_bump(version):

    # Major bump resets minor and patch
    version_major_bumped = version.bump_major()
    assert version_major_bumped.major == version.major + 1
    assert version_major_bumped.minor == 0
    assert version_major_bumped.patch == 0

    # Minor bump resets patch
    version_minor_bumped = version.bump_minor()
    assert version_minor_bumped.major == version.major
    assert version_minor_bumped.minor == version.minor + 1
    assert version_minor_bumped.patch == 0

    # Patch bump increments patch
    version_patch_bumped = version.bump_patch()
    assert version_patch_bumped.major == version.major
    assert version_patch_bumped.minor == version.minor
    assert version_patch_bumped.patch == version.patch + 1


@given(version=semver_versions(with_prerelease=True))
def test_semver_prerelease_bump(version: SemverVersion):
    import re
    
    # Prerelease bump increments prerelease
    version_prerelease_bumped = version.bump_prerelease()
    assert version_prerelease_bumped.major == version.major
    assert version_prerelease_bumped.minor == version.minor
    assert version_prerelease_bumped.patch == version.patch
    
    # Extract the numeric part of both original and bumped versions
    original_match = re.search(r'\d+$', version.prerelease)
    bumped_match = re.search(r'\d+$', version_prerelease_bumped.prerelease)
    if original_match and bumped_match:
        # Check that the number is incremented
        assert int(bumped_match.group(0)) > int(original_match.group(0))

    # Major prerelease bump increments major and resets prerelease
    version_major_prerelease_bumped = version.bump_major().bump_prerelease()
    assert version_major_prerelease_bumped.major == version.major + 1
    assert version_major_prerelease_bumped.minor == 0
    assert version_major_prerelease_bumped.patch == 0
    # Check that the number part is reset to 1
    assert re.search(r'1$', version_major_prerelease_bumped.prerelease)

    # Minor prerelease bump increments minor and resets prerelease
    version_minor_prerelease_bumped = version.bump_minor().bump_prerelease()
    assert version_minor_prerelease_bumped.major == version.major
    assert version_minor_prerelease_bumped.minor == version.minor + 1
    assert version_minor_prerelease_bumped.patch == 0
    # Check that the number part is reset to 1
    assert re.search(r'1$', version_minor_prerelease_bumped.prerelease)

    # Patch prerelease bump increments patch and resets prerelease
    version_patch_prerelease_bumped = version.bump_patch().bump_prerelease()
    assert version_patch_prerelease_bumped.major == version.major
    assert version_patch_prerelease_bumped.minor == version.minor
    assert version_patch_prerelease_bumped.patch == version.patch + 1
    # Check that the number part is reset to 1
    assert re.search(r'1$', version_patch_prerelease_bumped.prerelease)

    # Major bump resets prerelease
    version_major_bumped = version.bump_major()
    assert version_major_bumped.prerelease is None

    # Minor bump resets prerelease
    version_minor_bumped = version.bump_minor()
    assert version_minor_bumped.prerelease is None

    # Patch bump resets prerelease
    version_patch_bumped = version.bump_patch()
    assert version_patch_bumped.prerelease is None

@given(version=semver_versions())
def test_semver_version_parse_roundtrip(version):
    version_str = str(version)
    assert version == SemverVersion.from_string(version_str)
    
@pytest.mark.unittest
def test_bump_build():
    # Test without existing build
    version = SemverVersion(1, 2, 3)
    version_with_build = version.bump_build(include_sha=False)
    assert version_with_build.major == 1
    assert version_with_build.minor == 2
    assert version_with_build.patch == 3
    assert version_with_build.build == "1"
    
    # Test with existing build
    version_with_existing_build = SemverVersion(1, 2, 3, None, "5")
    version_with_bumped_build = version_with_existing_build.bump_build(include_sha=False)
    assert version_with_bumped_build.build == "6"
    
    # Test with existing build with multiple parts
    version_with_complex_build = SemverVersion(1, 2, 3, None, "7.abcd123")
    version_with_bumped_complex_build = version_with_complex_build.bump_build(include_sha=False)
    assert version_with_bumped_complex_build.build == "8"

@pytest.mark.unittest
@pytest.mark.parametrize('invalid_version', [
    '01.0.0', # leading zero
    '0.1.', # missing digit
    '0.01', # missing dot
    '0.0.0rc1', # missing hyphen in front of prerelease identifier
    # Note: The following are actually valid in SemVer 2.0.0:
    # '0.0.0-rc',
    # '0.0.0-rc0',
    # '0.0.0+rc1', # This is a build metadata, which is allowed
])
def test_semver_version_parsing_raises_on_invalid_semver(invalid_version):
    with pytest.raises(ValueError, match='Invalid semver format:'):
        SemverVersion.from_string(invalid_version)

@given(tag_string=tag_strings().filter(lambda x: x.strip() != ''))
def test_semver_parse_tags(tag_string: str):
    new_lines = len(tag_string.split('\n'))

    parsed = Semver()._parse_tags(tag_string=tag_string, prefix = None)

    current_tags = parsed['current']
    # No tags disappear when parsing
    assert len(current_tags['release']) + len(current_tags['prerelease']) + len(current_tags['other']) == new_lines

@given(current_release=semver_versions(), current_prerelease=semver_versions(with_prerelease=True))
def test_semver_get_next_semvers(current_release, current_prerelease):
    Semver()._get_next_semvers(current_release, current_prerelease)

@pytest.mark.unittest
@pytest.mark.parametrize(('prefix', 'expected'), [('v', 'v3.0.0'), ('', '3.0.0'), (' ', '3.0.0'), ('123', '1233.0.0')])
def test_bump_user_passed_prefix_included_over_config(prefix, expected):
    semver = Semver.from_json('gh_tt/tests/data/semver/semver_loaded_prefix.json')
    semver.set('semver_tags', semver._parse_tags(semver.get('tags'), prefix=None))
    
    result = semver.bump(level='major', message=None, prefix=prefix, execution_mode=ExecutionMode.DRY_RUN)
    
    assert expected in result
    assert semver.get('prefix') not in result

# We've completely removed support for custom prerelease suffixes
# All prerelease versions will always use 'alpha1' as the initial prerelease version

@pytest.mark.unittest
def test_semver_init_basic(capsys):
    """Test basic semver init with no existing tags"""
    semver = Semver()
    semver.set('semver_tags', {
        'current': {
            'release': [],
            'prerelease': [],
            'other': [],
        }
    })
    
    semver.init(version='1.0.0', message=None, prefix=None, execution_mode=ExecutionMode.DRY_RUN)
    output = capsys.readouterr().out
    
    assert 'git tag -a -m "Initial release 1.0.0"' in output

@pytest.mark.unittest
def test_semver_init_with_message(capsys):
    """Test semver init with an additional message"""
    semver = Semver()
    semver.set('semver_tags', {
        'current': {
            'release': [],
            'prerelease': [],
            'other': [],
        }
    })
    
    semver.init(version='2.0.0', message='First stable release', prefix=None, execution_mode=ExecutionMode.DRY_RUN)
    output = capsys.readouterr().out
    
    assert 'git tag -a -m "Initial release 2.0.0' in output
    assert 'First stable release' in output

@pytest.mark.unittest
def test_semver_init_with_prefix(capsys):
    """Test semver init with a prefix"""
    semver = Semver(prefix='v')
    semver.set('semver_tags', {
        'current': {
            'release': [],
            'prerelease': [],
            'other': [],
        }
    })
    
    semver.init(version='1.5.0', message=None, prefix='v', execution_mode=ExecutionMode.DRY_RUN)
    output = capsys.readouterr().out
    
    assert 'git tag -a -m "Initial release v1.5.0"' in output

@pytest.mark.unittest
def test_semver_init_fails_with_existing_release_tags():
    """Test that init fails when release tags already exist"""
    from gh_tt.utils import ContractError
    
    semver = Semver()
    # Create a mock release tag
    release_tag = type('SemverTag', (), {'version': SemverVersion(1, 0, 0)})()
    semver.set('semver_tags', {
        'current': {
            'release': [release_tag],
            'prerelease': [],
            'other': [],
        }
    })
    
    with pytest.raises(ContractError) as exc_info:
        semver.init(version='2.0.0', message=None, prefix=None)
    
    assert 'Cannot initialize semver' in str(exc_info.value)
    assert 'tags already exist' in str(exc_info.value)

@pytest.mark.unittest
def test_semver_init_fails_with_existing_prerelease_tags():
    """Test that init fails when prerelease tags already exist"""
    from gh_tt.utils import ContractError
    
    semver = Semver()
    # Create a mock prerelease tag
    prerelease_tag = type('SemverTag', (), {'version': SemverVersion(1, 0, 0, 'alpha1')})()
    semver.set('semver_tags', {
        'current': {
            'release': [],
            'prerelease': [prerelease_tag],
            'other': [],
        }
    })
    
    with pytest.raises(ContractError) as exc_info:
        semver.init(version='1.0.0', message=None, prefix=None)
    
    assert 'Cannot initialize semver' in str(exc_info.value)

@pytest.mark.unittest
def test_semver_init_succeeds_with_other_tags(capsys):
    """Test that init succeeds when only non-semver tags exist"""
    semver = Semver()
    semver.set('semver_tags', {
        'current': {
            'release': [],
            'prerelease': [],
            'other': ['some-old-tag', 'release-legacy'],
        }
    })
    
    semver.init(version='0.1.0', message=None, prefix=None, execution_mode=ExecutionMode.DRY_RUN)
    output = capsys.readouterr().out
    assert 'git tag -a -m "Initial release 0.1.0"' in output

@pytest.mark.unittest
def test_semver_init_invalid_version_format(capsys):
    """Test that init rejects invalid version formats"""
    semver = Semver()
    semver.set('semver_tags', {
        'current': {
            'release': [],
            'prerelease': [],
            'other': [],
        }
    })
    
    with pytest.raises(SystemExit) as exc_info:
        semver.init(version='invalid.version', message=None, prefix=None)
    
    assert exc_info.value.code == 1
    assert 'Invalid version format' in capsys.readouterr().err

@pytest.mark.unittest
def test_semver_init_with_all_parameters(capsys):
    """Test semver init with version, message, and prefix all set"""
    semver = Semver(prefix='release-')
    semver.set('semver_tags', {
        'current': {
            'release': [],
            'prerelease': [],
            'other': [],
        }
    })
    
    semver.init(
        version='3.2.1',
        message='Initial release with all features',
        prefix='release-',
        execution_mode=ExecutionMode.DRY_RUN
    )
    output = capsys.readouterr().out
    
    assert 'git tag -a -m "Initial release release-3.2.1' in output
    assert 'Initial release with all features' in output