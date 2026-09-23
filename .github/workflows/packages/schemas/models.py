"""V0.1 domain schemas."""
from datetime import date, datetime
from enum import Enum
from typing import Any, Literal
from pydantic import BaseModel, Field

class PolicyStatus(str, Enum): ACTIVE="ACTIVE"; EXPIRED="EXPIRED"; REPEALED="REPEALED"; UNKNOWN="UNKNOWN"
class ApplicationMode(str, Enum): FIXED_PERIOD="FIXED_PERIOD"; ROLLING="ROLLING"; BATCH="BATCH"; EVENT_TRIGGERED="EVENT_TRIGGERED"; UNKNOWN="UNKNOWN"
class ApplicationStatus(str, Enum): UPCOMING="UPCOMING"; OPEN="OPEN"; CLOSED="CLOSED"; UNKNOWN="UNKNOWN"
class Region(BaseModel): country:str="CN"; province:str|None=None; city:str|None=None; district:str|None=None
class Benefit(BaseModel): type:str; amount:float|None=None; currency:str="CNY"; description:str|None=None
class OfficialSource(BaseModel): url:str; publisher:str; publish_date:date|None=None
class Policy(BaseModel):
 policy_id:str; name:str; region:Region; department:str; categories:list[str]=[]; target_groups:list[str]=[]; benefit:Benefit|None=None; policy_status:PolicyStatus=PolicyStatus.UNKNOWN; effective_date:date|None=None; expiry_date:date|None=None; official_source:OfficialSource; last_verified_at:date
class ApplicationBatch(BaseModel):
 batch_id:str; policy_id:str; name:str; application_mode:ApplicationMode; start_at:datetime|None=None; end_at:datetime|None=None; status:ApplicationStatus=ApplicationStatus.UNKNOWN; application_url:str|None=None; last_verified_at:date
class Rule(BaseModel):
 type:Literal["condition","AND","OR","NOT"]; field:str|None=None; operator:str|None=None; value:Any=None; rules:list["Rule"]=[]
class UserProfile(BaseModel):
 age:int|None=None; education:str|None=None; city:str|None=None; hukou_city:str|None=None; graduation_year:int|None=None; employment_status:str|None=None; employment_city:str|None=None; social_security_months:int|None=None; owns_home:bool|None=None; marital_status:str|None=None; attributes:dict[str,Any]={}
class MatchResult(BaseModel):
 policy_id:str; status:Literal["eligible","ineligible","needs_more_info"]; matched:list[str]=[]; failed:list[dict[str,Any]]=[]; missing:list[str]=[]; explanation:str|None=None
Rule.model_rebuild()
