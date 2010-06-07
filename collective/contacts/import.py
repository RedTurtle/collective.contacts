# -*- coding: utf-8 -*-
import codecs
import csv
from zLOG import LOG, INFO, WARNING
from config import PROJECTNAME

from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from collective.contacts import contactsMessageFactory as _
from collective.contacts.interfaces import IImport, ISearch, IOrganization

class PersonCSVImport(object):
    implements(IImport)
    title = "CSV"
    
    def __init__(self, context):
        self.context = context
        
    def successMsg(self, imported):
        return _(u'Successfully imported ${number} persons', mapping={'number': imported})
        
    def importFile(self, file):
    
        LOG(PROJECTNAME, INFO, 'Starting the persons import process')
    
        portal_catalog = getToolByName(self.context, 'portal_catalog')
    
        # Now that we have all our configuration, we can start
    
        # First we set our results as an empty list, we will be loading
        # each user here
        results = []
    
        # we first make sure the content is in utf8
        reader = UnicodeReader(file)
    
        # Now we first load the headers
        headers = reader.next()
        rowLength = len(headers)
        counter = 0
    
        # Now i have to continue loading the rest of the persons
        for row in reader:
            # We now check that we have consistency in our CSV
            assert len(row) == rowLength
            result = {}
            for j in range(rowLength):
                result[headers[j]] = row[j]
    
            # And now, i have a new user, i add it to the results
            results.append(result)
            counter += 1
    
        path = '/'.join(self.context.getPhysicalPath())
        LOG(PROJECTNAME, INFO, '%s persons to be added to %s.' % (counter, path))
    
        counter = 0
    
        # I now have all persons in my results, so i should start adding them to
        # the site
        search = ISearch(self.context)
        for person in results:
            organization = None
            if person['organization']:
                organization = search.search({'object_provides': IOrganization.__identifier__,
                                              'id': person['organization']})
    
            if organization and len(organization)>1:
                LOG(PROJECTNAME, WARNING, 'There are %s organizations with the same id, '
                                          'I don\'t know with which one relate this person.' % len(organization))
                LOG(PROJECTNAME, WARNING, 'You will have to load the person with id %s '
                                          'manually.' % person['id'])
    
            elif ((organization and len(organization)==1) or
                 not person['organization']):
                if self.context.get(person['id']):
                    LOG(PROJECTNAME, WARNING, 'There\'s already a person with this id here.')
                    LOG(PROJECTNAME, WARNING, 'You will have to load the person with id '
                                              '%s manually.' % person['id'])
                else:
                    try:
                        self.context.invokeFactory('Person', person['id'])
                        new_person = self.context.get(person['id'])
                        for attr in person.keys():
                            if attr != 'id' and attr != 'organization':
                                setattr(new_person, attr, person[attr])
                            if (attr == 'organization' and
                                person['organization'] != ''):
                                new_person.setOrganization(organization[0])
    
                        counter += 1
                        portal_catalog.reindexObject(new_person)
    
                        LOG(PROJECTNAME, INFO, 'Successfully added %s.' % person['id'])
                    except:
                        LOG(PROJECTNAME, WARNING, 'There was an error while adding.')
                        LOG(PROJECTNAME, WARNING, 'You will have to load the person with id '
                                                  '%s manually.' % person['id'])
            else:
                LOG(PROJECTNAME, WARNING, 'There\'s no organization with id %s, '
                                          'make sure it exists before adding persons. '
                                          '%s not added' % (person['organization'], person['id']))
    
        LOG(PROJECTNAME, INFO, 'Successfully added %s persons to %s.' % (counter, path))
    
        return counter
    
class OrganizationCSVImport(object):
    implements(IImport)
    title = "CSV"
    
    def __init__(self, context):
        self.context = context
        
    def successMsg(self, imported):
        return _(u'Successfully imported ${number} organizations', mapping={'number': imported})
    
    def importFile(self, file):
        LOG(PROJECTNAME, INFO, 'Starting the organizations import process')
        # First we set our results as an empty list, we will be loading
        # each user here
        results = []
    
        portal_catalog = getToolByName(self.context, 'portal_catalog')
    
        # we first make sure the content is in utf8
        reader = UnicodeReader(file)
    
        # Now we first load the headers
        headers = reader.next()
        rowLength = len(headers)
        counter = 0
    
        # Now i have to continue loading the rest of the persons
        for row in reader:
            # We now check that we have consistency in our CSV
            assert len(row) == rowLength
            result = {}
            for j in range(rowLength):
                result[headers[j]] = row[j]
    
            # And now, i have a new user, i add it to the results
            results.append(result)
            counter += 1
    
        path = '/'.join(self.context.getPhysicalPath())
        LOG(PROJECTNAME, INFO, '%s organizations to be added to %s.' % (counter, path))
    
        counter = 0
        # I now have all persons in my results, so i should start adding them to site
        for organization in results:
            if self.context.get(organization['id']):
    
                LOG(PROJECTNAME, WARNING, 'There\'s already an organization with this id here.')
                LOG(PROJECTNAME, WARNING, 'You will have to load the organization with id '
                                          '%s manually.' % organization['id'])
    
            else:
                try:
                    self.context.invokeFactory('Organization', organization['id'])
                    new_organization = self.context.get(organization['id'])
                    for attr in organization.keys():
                        if attr != 'id':
                            setattr(new_organization, attr, organization[attr])
                    counter += 1
                    portal_catalog.reindexObject(new_organization)
                    LOG(PROJECTNAME, INFO, 'Successfully added %s.' % organization['id'])
                except:
                    LOG(PROJECTNAME, WARNING, 'There was an error while adding.')
                    LOG(PROJECTNAME, WARNING, 'You will have to load the organization with id '
                                              '%s manually.' % organization['id'])
                    
        LOG(PROJECTNAME, INFO, 'Successfully added %s organizations to %s.' % (counter, path))
        return counter

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

def strToInt(data):
    return int(data)

def strToFloat(data):
    return float(data)

def removeExtension(filename):
    if '.' in filename:
        filename = filename[:filename.rfind('.')]

    return filename