# -*- coding: utf-8 -*-
import unittest
from datetime import timedelta
from copy import deepcopy

from openprocurement.api.utils import get_now
from openprocurement.auctions.rubble.tests.base import (
    BaseAuctionWebTest, test_bids, test_lots, test_organization, test_features_auction_data,
    test_financial_auction_data, test_financial_bids, test_financial_organization, test_auction_data
)

from openprocurement.auctions.core.tests.auctions import (
    AuctionAuctionResourceTestMixin,
    AuctionLotAuctionResourceTestMixin,
    AuctionMultipleLotAuctionResourceTestMixin
)
from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.rubble.constants import DEFAULT_PROCUREMENT_METHOD_TYPE_FINANCIAL
from openprocurement.auctions.rubble.tests.blanks.auction_blanks import (
    # AuctionAuctionResourceTest
    post_auction_auction,
    # AuctionLotAuctionResourceTest
    post_auction_auction_lot,
    # AuctionMultipleLotAuctionResourceTest
    post_auction_auction_2_lots,
)
from openprocurement.auctions.core.tests.blanks.auction_blanks import (
    # AuctionSameValueAuctionResourceTest
    post_auction_auction_not_changed,
    post_auction_auction_reversed,
    # AuctionFeaturesAuctionResourceTest
    get_auction_features_auction
)

class AuctionAuctionResourceTest(BaseAuctionWebTest, AuctionAuctionResourceTestMixin):
    #initial_data = auction_data
    initial_status = 'active.tendering'
    initial_bids = test_bids

    test_post_auction_auction = snitch(post_auction_auction)


class AuctionSameValueAuctionResourceTest(BaseAuctionWebTest):
    initial_status = 'active.auction'
    initial_bids = [
        {
            "tenderers": [
                test_organization
            ],
            "value": {
                "amount": 469,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            },
            'qualified': True
        }
        for i in range(3)
    ]
    test_post_auction_auction_not_changed = snitch(post_auction_auction_not_changed)
    test_post_auction_auction_reversed = snitch(post_auction_auction_reversed)


@unittest.skip("option not available")
class AuctionLotAuctionResourceTest(BaseAuctionWebTest, AuctionLotAuctionResourceTestMixin):
    initial_lots = test_lots

    test_post_auction_auction_lots = snitch(post_auction_auction_lot)



@unittest.skip("option not available")
class AuctionMultipleLotAuctionResourceTest(BaseAuctionWebTest, AuctionMultipleLotAuctionResourceTestMixin):
    initial_lots = 2 * test_lots
    test_post_auction_auction_2_lots = snitch(post_auction_auction_2_lots)


@unittest.skip("option not available")
class AuctionFeaturesAuctionResourceTest(BaseAuctionWebTest):
    initial_data = test_features_auction_data
    initial_status = 'active.auction'
    initial_bids = [
        {
            "parameters": [
                {
                    "code": i["code"],
                    "value": 0.1,
                }
                for i in test_features_auction_data['features']
            ],
            "tenderers": [
                test_organization
            ],
            "value": {
                "amount": 469,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            },
            'qualified': True
        },
        {
            "parameters": [
                {
                    "code": i["code"],
                    "value": 0.15,
                }
                for i in test_features_auction_data['features']
            ],
            "tenderers": [
                test_organization
            ],
            "value": {
                "amount": 479,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            }
        }
    ]

    test_get_auction_features_auction = snitch(get_auction_features_auction)

class FinancialAuctionAuctionResourceTest(AuctionAuctionResourceTest):
    initial_bids = test_financial_bids
    initial_data = test_financial_auction_data


class FinancialAuctionSameValueAuctionResourceTest(AuctionSameValueAuctionResourceTest):
    initial_data = test_financial_auction_data
    initial_bids = [
        {
            "tenderers": [
                test_financial_organization
            ],
            "value": {
                "amount": 469,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            },
            'qualified': True,
            'eligible': True
        }
        for i in range(3)
    ]


@unittest.skip("option not available")
class FinancialAuctionLotAuctionResourceTest(AuctionLotAuctionResourceTest):
    initial_data = test_financial_auction_data
    initial_bids = test_financial_bids


@unittest.skip("option not available")
class FinancialAuctionMultipleLotAuctionResourceTest(AuctionMultipleLotAuctionResourceTest):
    initial_bids = test_financial_bids
    initial_data = test_financial_auction_data


@unittest.skip("option not available")
class FinancialAuctionFeaturesAuctionResourceTest(AuctionFeaturesAuctionResourceTest):
    initial_data = deepcopy(test_features_auction_data)
    initial_data["procurementMethodType"] = DEFAULT_PROCUREMENT_METHOD_TYPE_FINANCIAL
    initial_bids = [
        {
            "parameters": [
                {
                    "code": i["code"],
                    "value": 0.1,
                }
                for i in test_features_auction_data['features']
            ],
            "tenderers": [
                test_financial_organization
            ],
            "value": {
                "amount": 469,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            },
            'qualified': True,
            'eligible': True
        },
        {
            "parameters": [
                {
                    "code": i["code"],
                    "value": 0.15,
                }
                for i in test_features_auction_data['features']
            ],
            "tenderers": [
                test_financial_organization
            ],
            "value": {
                "amount": 479,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            },
            'qualified': True,
            'eligible': True
        }
    ]



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionAuctionResourceTest))
    suite.addTest(unittest.makeSuite(AuctionSameValueAuctionResourceTest))
    suite.addTest(unittest.makeSuite(AuctionFeaturesAuctionResourceTest))
    suite.addTest(unittest.makeSuite(FinancialAuctionAuctionResourceTest))
    suite.addTest(unittest.makeSuite(FinancialAuctionSameValueAuctionResourceTest))
    suite.addTest(unittest.makeSuite(FinancialAuctionFeaturesAuctionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
