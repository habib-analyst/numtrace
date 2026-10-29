"""Three separate verdicts, mirroring the paper's split (in our own code):

- value:   claimed number equals a source record value for that ticker/period,
           OR equals the arithmetic sum of the asked scope's records
           (digits/arithmetic match the source).
- binding: claimed number, as asserted for the asked scope, equals the reference
           (entity + concept + period + unit + scope all match).
- support: the cited source records actually back BOTH value and binding:
           for a group claim, citations must be exactly the group's member
           records for that ticker/period; for a direct claim, the single firm
           record.

RNWA (right number, wrong account) = value pass AND binding fail.
Joint pass = value pass AND binding pass.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    value: int
    asserted_scope: str  # e.g. "GROUP-001 total" or "FIRM-001-0"
    citations: tuple  # doc_ids cited


@dataclass(frozen=True)
class Verdict:
    value: bool
    binding: bool
    support: bool

    @property
    def rnwa(self) -> bool:
        return self.value and not self.binding

    @property
    def joint(self) -> bool:
        return self.value and self.binding


def audit_group_claim(claim: Claim, records, question) -> Verdict:
    """records: full corpus. question: GroupQuestion."""
    same_slice = [r for r in records
                  if r.ticker == question.ticker and r.period == question.period]
    member = [r for r in same_slice if r.group == question.group]
    member_values = {r.shares for r in member}
    all_values = {r.shares for r in same_slice}
    value = claim.value in all_values or claim.value == question.reference
    binding = (claim.value == question.reference
               and claim.asserted_scope == f"{question.group} total")
    support = (binding and claim.value == question.reference
               and set(claim.citations) == {r.doc_id for r in member})
    return Verdict(value=value, binding=binding, support=support)


def audit_direct_claim(claim: Claim, records, question) -> Verdict:
    target = [r for r in records if r.firm == question.firm
              and r.ticker == question.ticker and r.period == question.period]
    assert len(target) == 1
    r = target[0]
    value = claim.value == r.shares
    binding = value and claim.asserted_scope == question.firm
    support = binding and tuple(claim.citations) == (r.doc_id,)
    return Verdict(value=value, binding=binding, support=support)
