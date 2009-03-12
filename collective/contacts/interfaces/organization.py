from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from collective.contacts import contactsMessageFactory as _

class IOrganization(Interface):
    """Contact information of an organization"""
    
    # -*- schema definition goes here -*-

    address = schema.TextLine(
        title=_(u"Address"),
        required=False,
        description=_(u"Organization's address"),
    )

    city = schema.TextLine(
        title=_(u"City"),
        required=False,
        description=_(u"Organization's city"),
    )

    zip = schema.TextLine(
        title=_(u"ZIP"),
        required=False,
        description=_(u"Organization's ZIP"),
    )

    country = schema.TextLine(
        title=_(u"Country"),
        required=False,
        description=_(u"Organization's country"),
    )

    extra_address = schema.TextLine(
        title=_(u"Extra Address Info"),
        required=False,
        description=_(u"Organization's extra address information."),
    )

    phone = schema.TextLine(
        title=_(u"Phone Number"),
        required=False,
        description=_(u"Organization's phone number"),
    )

    fax = schema.TextLine(
        title=_(u"Fax Number"),
        required=False,
        description=_(u"Organization's fax number"),
    )

    email = schema.TextLine(
        title=_(u"E-mail address"),
        required=False,
        description=_(u"Organization's e-mail address"),
    )

    email2 = schema.TextLine(
        title=_(u"2nd E-mail address"),
        required=False,
        description=_(u"Organization's 2nd e-mail address"),
    )

    email3 = schema.TextLine(
        title=_(u"3rd E-mail address"),
        required=False,
        description=_(u"Organization's 3rd e-mail address"),
    )

    web = schema.TextLine(
        title=_(u"Web"),
        required=False,
        description=_(u"Organization's web page or blog"),
    )

    sector = schema.TextLine(
        title=_(u"Sector"),
        required=False,
        description=_(u"Organization's sector"),
    )

    text = schema.TextLine(
        title=_(u"Text"),
        required=False,
    )