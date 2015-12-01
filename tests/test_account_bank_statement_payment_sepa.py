# This file is part of the account_bank_statement_payment_sepa module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AccountBankStatementPaymentSepaTestCase(ModuleTestCase):
    'Test Account Bank Statement Payment Sepa module'
    module = 'account_bank_statement_payment_sepa'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountBankStatementPaymentSepaTestCase))
    return suite