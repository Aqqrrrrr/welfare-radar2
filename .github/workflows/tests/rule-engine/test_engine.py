import sys
sys.path.insert(0,"packages")
from schemas.models import Rule, UserProfile
from rule_engine import match

def test_and_eligible():
 r=Rule(type="AND",rules=[Rule(type="condition",field="age",operator=">=",value=18),Rule(type="condition",field="city",operator="==",value="深圳")])
 x=match("P1",r,UserProfile(age=24,city="深圳")); assert x.status=="eligible"
def test_missing():
 r=Rule(type="condition",field="education",operator="==",value="本科")
 assert match("P1",r,UserProfile()).status=="needs_more_info"
def test_or():
 r=Rule(type="OR",rules=[Rule(type="condition",field="city",operator="==",value="广州"),Rule(type="condition",field="city",operator="==",value="深圳")])
 assert match("P1",r,UserProfile(city="深圳")).status=="eligible"
