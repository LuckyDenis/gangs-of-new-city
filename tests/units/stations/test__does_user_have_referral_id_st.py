# coding: utf8

import pytest
from app.core.stations import DoesUserHaveReferralIdSt
from app.core.statuses import Statuses as Code

REFERRAL_ID = 123451231
VOID_REFERRAL_ID = None
KEY_REFERRAL_ID = "referral_id"
STATUSES = [
    Code.USER_DOSE_NOT_HAVE_REFERRAL_ID,
    Code.EMERGENCY_STOP
]


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled(train):
    train.data[KEY_REFERRAL_ID] = REFERRAL_ID
    await DoesUserHaveReferralIdSt(train).traveled()
    assert train.status is Code.USER_HAS_REFERRAL_ID


@pytest.mark.unit
@pytest.mark.core
@pytest.mark.stations
async def test__traveled_not_ref_id(train):
    train.data[KEY_REFERRAL_ID] = VOID_REFERRAL_ID
    await DoesUserHaveReferralIdSt(train).traveled()

    statuses = train["__state__"]["statuses"]
    assert statuses[-2:] == STATUSES
