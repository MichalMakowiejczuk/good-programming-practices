from payment_gateway import (
    PaymentGateway,
    TransactionResult,
    TransactionStatus,
    NetworkException,
    PaymentException,
    RefundException,
)


class MockPaymentGateway(PaymentGateway):
    def __init__(self):
        self.charged_transactions = []
        self.refunded_transactions = []
        self.status_queries = []

        self.raise_network_exception = False
        self.raise_payment_exception = False
        self.raise_refund_exception = False
        self.transaction_status = TransactionStatus.PENDING

    def charge(self, user_id: str, amount: float) -> TransactionResult:
        if self.raise_network_exception:
            raise NetworkException("Network error during charge.")
        if self.raise_payment_exception:
            raise PaymentException("Payment failed due to insufficient funds.")

        transaction_id = f"txn-{user_id}-{amount}"
        self.charged_transactions.append((user_id, amount))

        return TransactionResult(
            success=True, transaction_id=transaction_id, message="Payment successful"
        )

    def refund(self, transaction_id: str) -> TransactionResult:
        if self.raise_network_exception:
            raise NetworkException("Network error during refund.")
        if self.raise_refund_exception:
            raise RefundException("Refund failed due to invalid transaction.")

        self.refunded_transactions.append(transaction_id)

        return TransactionResult(
            success=True, transaction_id=transaction_id, message="Refund successful"
        )

    def get_status(self, transaction_id: str) -> TransactionStatus:
        if self.raise_network_exception:
            raise NetworkException("Network error during get_status.")

        self.status_queries.append(transaction_id)

        return self.transaction_status
