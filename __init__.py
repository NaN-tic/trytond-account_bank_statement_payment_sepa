# This file is part of account_bank_statement_payment_sepa module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import statement


def register():
    Pool.register(
        statement.StatementLine,
        module='account_bank_statement_payment_sepa', type_='model')
