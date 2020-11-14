# coding: utf8

import pytest
from app.core.stations import DoesUserHaveReferralIdSt
from app.core.statuses import Statuses as Code

REFERRAL_ID = 123451231
VOID_REFERRAL_ID = None
KEY_REFERRAL_ID = "referral_id"


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(train):
    train.data[KEY_REFERRAL_ID] = REFERRAL_ID
    status = await DoesUserHaveReferralIdSt.traveled(train)
    assert status is Code.IS_OK


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_not_ref_id(train):
    train.data[KEY_REFERRAL_ID] = VOID_REFERRAL_ID
    status = await DoesUserHaveReferralIdSt.traveled(train)

    assert status is Code.EMERGENCY_STOP
