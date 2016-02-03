# This file is part of account_bank_statement_payment_sepa module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from sql import operators
from sql.aggregate import Sum
from decimal import Decimal
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__metaclass__ = PoolMeta
__all__ = ['StatementLine']

_ZERO = Decimal('0.0')


class StatementLine:
    __name__ = 'account.bank.statement.line'

    def _search_payments(self, amount):
        pool = Pool()
        Payment = pool.get('account.payment')
        Journal = pool.get('account.payment.journal')
        Mandate = pool.get('account.payment.sepa.mandate')
        payment = Payment.__table__()
        mandate = Mandate.__table__()

        payments = super(StatementLine, self)._search_payments(amount)
        if len(payments):
            return payments

        search_amount = abs(amount)
        if search_amount == _ZERO:
            return []

        kind = 'receivable' if amount > _ZERO else 'payable'
        journals = Journal.search([('currency', '=', self.statement_currency),
            ('process_method', 'like', 'sepa%')])
        journals = [j.id for j in journals]
        search_amount = Payment.amount._domain_value('=', search_amount)

        if kind == 'receivable':
            payment_mandate = payment.join(mandate,
                condition=payment.sepa_mandate == mandate.id)
            subquery = payment_mandate.select(payment.sepa_mandate,
                mandate.type, mandate.scheme,
                group_by=(payment.sepa_mandate, mandate.type, mandate.scheme),
                where=(payment.kind == 'receivable')
                )

            query = payment.join(subquery,
                condition=payment.sepa_mandate == subquery.sepa_mandate)
            query = query.select(payment.group, payment.date,
                subquery.type, subquery.scheme,
                group_by=(payment.group, payment.date, subquery.type,
                    subquery.scheme),
                having=operators.Equal(Sum(payment.amount), search_amount),
                where=(payment.kind == 'receivable') & (payment.group != None)
                    & (payment.journal.in_(journals)),
                order_by=payment.date.desc,
                )

        else:
            query = payment.select(payment.group, payment.date,
                group_by=(payment.group, payment.date),
                having=operators.Equal(Sum(payment.amount), search_amount),
                where=(payment.kind == 'payable') & (payment.group != None)
                    & (payment.journal.in_(journals)),
                order_by=payment.date.desc,
                )

        cursor = Transaction().cursor
        cursor.execute(*query)
        res = cursor.fetchall()
        domains = [[('group', '=', r[0]), ('date', '=', r[1])] for r in res]
        for domain, r in zip(domains, res):
            payments = Payment.search(domain)
            if kind == 'receivable':
                payments = [p for p in payments if p.sepa_mandate.type == r[2]
                    and p.sepa_mandate.scheme == r[3]]
            found = True
            for payment in payments:
                if payment.line and payment.line.reconciliation:
                    found = False
                    break
            if found:
                break

        return payments
