######################################################################
#
# File: test/integration/test_bucket.py
#
# Copyright 2024 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################
import pytest


def test_bucket_notification_rules(bucket, b2_api):
    if 'writeBucketNotifications' not in b2_api.account_info.get_allowed()['capabilities']:
        pytest.skip('Test account does not have writeBucketNotifications capability')

    assert bucket.set_notification_rules([]) == []
    assert bucket.get_notification_rules() == []

    notification_rule = {
        "eventTypes": ["b2:ObjectCreated:*"],
        "isEnabled": True,
        "name": "test-rule",
        "objectNamePrefix": "",
        "targetConfiguration":
            {
                "customHeaders": [],
                "targetType": "webhook",
                "url": "https://example.com/webhook",
                "hmacSha256SigningSecret": "stringOf32AlphaNumericCharacters",
            }
    }

    set_notification_rules = bucket.set_notification_rules([notification_rule])
    assert set_notification_rules == bucket.get_notification_rules()
    assert set_notification_rules == [
        {
            **notification_rule, "isSuspended": False,
            "suspensionReason": ""
        }
    ]
    assert bucket.set_notification_rules([]) == []
