"""Utility functions for design by contract programming."""


class ContractError(Exception):
    """Exception raised when a contract is violated.
    
    Contract violations are user-facing errors representing invalid program state
    or precondition failures, distinct from unexpected runtime errors.
    """


def assert_contract(*, contract: bool, msg: str, hint: str | None = None) -> None:
    """Assert a contract condition using design by contract principles.
    
    Raises a ContractError with a clean, user-friendly message if the contract is violated.
    
    Args:
        contract: Boolean condition that must be True for the contract to hold
        msg: The main error message describing what went wrong
        hint: Optional helpful hint or instruction for resolving the issue
        
    Raises:
        ContractError: If contract is False, with formatted message including hint if provided
        
    Example:
        >>> from gh_tt.utils import assert_contract
        >>> assert_contract(version is not None, "No version found", "Run 'init' first")
    """
    if not contract:
        error_msg = f"❌ {msg}"
        if hint:
            error_msg += f"\n💡 {hint}"
        raise ContractError(error_msg)
