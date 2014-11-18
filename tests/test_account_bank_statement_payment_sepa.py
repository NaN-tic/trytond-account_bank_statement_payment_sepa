#!/usr/bin/env python
# This file is part of account_bank_statement_payment_sepa module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_depends


class AccountBankStatementPaymentSEPATestCase(unittest.TestCase):
    'Test Account Bank Statement Payment SEPA module'

    def setUp(self):
        trytond.tests.test_tryton.install_module(
            'account_bank_statement_payment_sepa')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountBankStatementPaymentSEPATestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
