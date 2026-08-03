from django.test import TestCase
from .models import Address, Organization, OrganizationMember, User


class CustomerAccountModelTests(TestCase):
    def test_customer_uses_email_as_login_and_can_join_organization(self):
        customer = User.objects.create_user(email="buyer@example.com", password="pass12345")
        organization = Organization.objects.create(name="Acme Foods", gstin="29ABCDE1234F1Z5")
        membership = OrganizationMember.objects.create(organization=organization, user=customer, role="owner")
        address = Address.objects.create(user=customer, organization=organization, recipient_name="Asha Kumar", phone="9000000000", line1="1 Market Road", city="Bengaluru", state="Karnataka", postal_code="560001")
        self.assertEqual(customer.get_username(), "buyer@example.com")
        self.assertEqual(membership.organization, organization)
        self.assertEqual(address.organization, organization)
