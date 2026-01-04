#!/usr/bin/env python3

import sys

from gh_tt.classes.gitter import Gitter
from gh_tt.modules.tt_handlers import COMMAND_HANDLERS
from gh_tt.modules.tt_parser import tt_parse
from gh_tt.utils import ContractError


def main():
    args = tt_parse(sys.argv[1:])

    Gitter.set_verbose(value=args.verbose)
    Gitter.validate_gh_version()

    if args.version:
        Gitter.version()
        sys.exit(0)

    Gitter.read_cache()
    # Gitter.validate_gh_scope(scope='project') this check causes more problems than it solves
    
    try:
        # Execute the appropriate command handler
        if args.command in COMMAND_HANDLERS:
            COMMAND_HANDLERS[args.command](args)
    except ContractError as e:
        print(f"{e}", file=sys.stderr)
        if Gitter.verbose:
            tb = e.__traceback__
            # Go back one frame from the innermost to skip the raise line in utils.py
            # and point to where assert_contract was actually called
            while tb.tb_next and tb.tb_next.tb_next:
                tb = tb.tb_next
            filename = tb.tb_frame.f_code.co_filename
            lineno = tb.tb_lineno
            print(f"🔦 @ {filename}:{lineno}", file=sys.stderr)
        sys.exit(1)
            
    Gitter.write_cache()            
    sys.exit(0)
