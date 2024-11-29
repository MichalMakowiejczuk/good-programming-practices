import unittest
from payment_gateway import (
    TransactionResult,
    TransactionStatus,
    NetworkException,
    PaymentException,
    RefundException,
)
from payment_processor import PaymentProcessor
from mock_payment_gateway import MockPaymentGateway


class PaymentProcessorTest(unittest.TestCase):
    def setUp(self):
        self.payment_gateway = MockPaymentGateway()
        self.payment_processor = PaymentProcessor(self.payment_gateway)

    def test_process_payment_successful(self):
        result = self.payment_processor.process_payment("user123", 100.0)
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Payment successful")
        self.assertIn(("user123", 100.0), self.payment_gateway.charged_transactions)

    def test_process_payment_network_exception(self):
        self.payment_gateway.raise_network_exception = True
        result = self.payment_processor.process_payment("user123", 100.0)
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Payment failed due to an error.")
        self.assertNotIn(("user123", 100.0), self.payment_gateway.charged_transactions)

    def test_process_payment_payment_exception(self):
        self.payment_gateway.raise_payment_exception = True
        result = self.payment_processor.process_payment("user123", 100.0)
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Payment failed due to an error.")
        self.assertNotIn(("user123", 100.0), self.payment_gateway.charged_transactions)

    def test_process_payment_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.payment_processor.process_payment("user123", -50)

    def test_get_payment_status_empty_transaction_id(self):
        with self.assertRaises(ValueError):
            self.payment_processor.get_payment_status("")

    def test_refund_payment_successful(self):
        result = self.payment_processor.refund_payment("txn123")
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Refund successful")
        self.assertIn("txn123", self.payment_gateway.refunded_transactions)

    def test_refund_payment_refund_exception(self):
        self.payment_gateway.raise_refund_exception = True
        result = self.payment_processor.refund_payment("txn123")
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Refund failed due to an error.")
        self.assertNotIn("txn123", self.payment_gateway.refunded_transactions)

    def test_get_payment_status_successful(self):
        self.payment_gateway.transaction_status = TransactionStatus.COMPLETED
        status = self.payment_processor.get_payment_status("txn123")
        self.assertEqual(status, TransactionStatus.COMPLETED)
        self.assertIn("txn123", self.payment_gateway.status_queries)

    def test_get_payment_status_network_exception(self):
        self.payment_gateway.raise_network_exception = True
        status = self.payment_processor.get_payment_status("txn123")
        self.assertEqual(status, TransactionStatus.FAILED)
        self.assertNotIn("txn123", self.payment_gateway.status_queries)


if __name__ == "__main__":
    unittest.main()
