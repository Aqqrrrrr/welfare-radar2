from typing import Any
from packages.schemas.models import Rule, UserProfile, MatchResult

def evaluate(rule: Rule, profile: UserProfile) -> tuple[bool,list[str],list[dict[str,Any]],list[str]]:
    if rule.type in ("AND","OR","NOT"):
        results=[evaluate(r,profile) for r in rule.rules]
        if rule.type=="AND": ok=all(x[0] for x in results)
        elif rule.type=="OR": ok=any(x[0] for x in results)
        else: ok=not results[0][0]
        return ok, [f for x in results for f in x[1]], [f for x in results for f in x[2]], [f for x in results for f in x[3]]
    actual=getattr(profile, rule.field, None)
    if actual is None: actual=profile.attributes.get(rule.field)
    if actual is None: return False,[],[],[rule.field]
    op=rule.operator; expected=rule.value
    try:
        ok = (actual == expected if op == "==" else actual != expected if op == "!=" else actual > expected if op == ">" else actual >= expected if op == ">=" else actual < expected if op == "<" else actual <= expected if op == "<=" else actual in expected if op == "in" else expected in actual if op == "contains" else False)
    except (KeyError,TypeError): ok=False
    if ok:return True,[rule.field],[],[]
    return False,[],[{"field":rule.field,"operator":op,"required":expected,"actual":actual}],[]

def match(policy_id:str, rule:Rule, profile:UserProfile)->MatchResult:
    ok,matched,failed,missing=evaluate(rule,profile)
    status="eligible" if ok else ("needs_more_info" if missing else "ineligible")
    return MatchResult(policy_id=policy_id,status=status,matched=matched,failed=failed,missing=missing)

