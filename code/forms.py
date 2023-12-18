from wtforms import Form
from wtforms import IntegerField, TextAreaField, SubmitField, RadioField, SelectField, StringField, \
    IntegerRangeField
from wtforms import validators, ValidationError


class ReservationForm(Form):
    firstname = StringField("First name", [validators.InputRequired("Zadejte své jméno.")])
    lastname = StringField("Last name", [validators.InputRequired("Zadejte své příjmení.")])
    email = StringField("Email", [validators.InputRequired("Zadejte svou e-mailovou adresu."),
                                  validators.Email("Zadejte svou e-mailovou adresu.")])
    phone = IntegerField("Phone number", [validators.InputRequired("Zadejte své telefonní číslo.")])

    guest = IntegerField("Guests")

    submit = SubmitField("Submit")


class OrderInfoForm(Form):
    orderfirstname = StringField("First name", [validators.InputRequired("* Zadejte své jméno.")])
    orderlastname = StringField("Last name", [validators.InputRequired("* Zadejte své příjmení.")])
    orderemail = StringField("Email", [validators.InputRequired("* Zadejte svou e-mailovou adresu."),
                                       validators.Email("* Zadejte svou e-mailovou adresu.")])
    orderphone = IntegerField("Phone number", [validators.InputRequired("* Zadejte své telefonní číslo.")])
    deliveryservise = RadioField("Delivery servise", choices=[('f', 'Foodora'), ('g', 'Glovo')])
    city = RadioField("City", choices=[('u', 'Ústí nad Labem'), ('d', 'Děčín')])
    address = StringField("Address", [validators.InputRequired("* Zadejte adresu")])
    paymethod = RadioField("Pay method", choices=[('p', 'Po přijetí'), ('t', 'Teď')])
    ordersubmit = SubmitField("Confirm the order")


class OrderForm(Form):
    delproductsubmit = SubmitField("Delete from Order")
    gotomenusubmit = SubmitField("Back to shopping")
    gotoorderinfosubmit = SubmitField("Proceed to Checkout")


class MenuForm(Form):
    count = IntegerField("", [validators.InputRequired("You should write count products")],
                         description='Input count products', default=1)

    menusubmit = SubmitField("Add to order")


class AddOrderForm(Form):
    gotomenusubmit = SubmitField("Back to shopping")
    gotoordersubmit = SubmitField("Go to order")


class SaveOrderForm(Form):
    gotomenusubmit = SubmitField("Back to shopping")
    gotoordersubmit = SubmitField("Go to order")


class DelOrderForm(Form):
    gotomenusubmit = SubmitField("Back to shopping")
    gotoordersubmit = SubmitField("Go to order")