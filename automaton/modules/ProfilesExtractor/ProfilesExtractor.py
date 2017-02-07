import sys
import time
from utils import LogHelper, LinkedinHelper

class ProfilesExtractor(object):

	TIMEOUT = 7
	MODE = 'LOGGED'

	SECTIONS = {}
	FIELDS = {}
	CONTAINER = {}

	SITE_URL = 'https://www.linkedin.com'

	# PUBLIC

	CONTAINER['PUBLIC'] = '#profile'
	SECTIONS['PUBLIC'] = {}
	FIELDS['PUBLIC'] = {}
	SECTIONS['PUBLIC']['NAME'] = {'selector':'#name', 'type':'text', 'quantity':'single'}
	SECTIONS['PUBLIC']['IMAGE'] = {'selector':'.profile-picture img', 'type':'attr', 'attr':'src', 'quantity':'single'}
	SECTIONS['PUBLIC']['CONNECTIONS'] = {'selector':'.member-connections', 'type':'text', 'quantity':'single'}
	SECTIONS['PUBLIC']['TITLE'] = {'selector':'p.title', 'type':'text', 'quantity':'single'}
	SECTIONS['PUBLIC']['LOCATION'] = {'selector':'.locality', 'type':'text', 'quantity':'single'}
	SECTIONS['PUBLIC']['INDUSTRY'] = {'selector':'#demographics dd.descriptor:nth-child(2)', 'type':'text', 'quantity':'single'}
	SECTIONS['PUBLIC']['RECOMMENDATIONS_NUMBER'] = {'selector':'.extra-info > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > strong:nth-child(1)', 'type':'text', 'quantity':'single'}
	SECTIONS['PUBLIC']['SUMMARY'] = {'selector':'#summary .description', 'type':'text', 'quantity':'single'}
	
	SECTIONS['PUBLIC']['BRIEF_CURRENT'] = {'selector':'[data-section="currentPositionsDetails"] li', 'quantity':'multiple'}
	FIELDS['PUBLIC']['BRIEF_CURRENT'] = {}
	FIELDS['PUBLIC']['BRIEF_CURRENT']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['PUBLIC']['BRIEF_CURRENT']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['PUBLIC']['BRIEF_PREVIOUS'] = {'selector':'[data-section="pastPositionsDetails"] li', 'quantity':'multiple'}
	FIELDS['PUBLIC']['BRIEF_PREVIOUS'] = {}
	FIELDS['PUBLIC']['BRIEF_PREVIOUS']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['PUBLIC']['BRIEF_PREVIOUS']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['PUBLIC']['BRIEF_EDUCATION'] = {'selector':'[data-section="educationsDetails"] li', 'quantity':'multiple'}
	FIELDS['PUBLIC']['BRIEF_EDUCATION'] = {}
	FIELDS['PUBLIC']['BRIEF_EDUCATION']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['PUBLIC']['BRIEF_EDUCATION']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['PUBLIC']['WEBSITES'] = {'selector':'[data-section="websites"] li', 'quantity':'multiple'}
	FIELDS['PUBLIC']['WEBSITES'] = {}
	FIELDS['PUBLIC']['WEBSITES']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['PUBLIC']['WEBSITES']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['PUBLIC']['POSTS'] = {'selector':'.post', 'quantity':'multiple'}
	FIELDS['PUBLIC']['POSTS'] = {}
	FIELDS['PUBLIC']['POSTS']['NAME'] = {'selector':'.item-title', 'type':'text'}
	FIELDS['PUBLIC']['POSTS']['URL'] = {'selector':'.item-title a', 'type':'attr', 'attr':'href'}
	FIELDS['PUBLIC']['POSTS']['IMG'] = {'selector':'img', 'type':'attr', 'attr':'src'}
	FIELDS['PUBLIC']['POSTS']['DATE'] = {'selector':'.time', 'type':'text'}

	SECTIONS['PUBLIC']['EXPERIENCE'] = {'selector':'.position', 'quantity':'multiple'}
	FIELDS['PUBLIC']['EXPERIENCE'] = {}
	FIELDS['PUBLIC']['EXPERIENCE']['TITLE'] = {'selector':'.item-title', 'type':'text'}
	FIELDS['PUBLIC']['EXPERIENCE']['TITLE_URL'] = {'selector':'.item-title a', 'type':'attr', 'attr':'href'}
	FIELDS['PUBLIC']['EXPERIENCE']['IMG'] = {'selector':'img', 'type':'attr', 'attr':'src'}
	FIELDS['PUBLIC']['EXPERIENCE']['COMPANY'] = {'selector':'.item-subtitle a', 'type':'text'}
	FIELDS['PUBLIC']['EXPERIENCE']['COMPANY_URL'] = {'selector':'.item-subtitle a', 'type':'attr', 'attr':'href'}
	FIELDS['PUBLIC']['EXPERIENCE']['DATE'] = {'selector':'.date-range', 'type':'text'}
	FIELDS['PUBLIC']['EXPERIENCE']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}
	
	SECTIONS['PUBLIC']['VOLUNTEER_POSITION'] = {'selector':'#volunteering .position', 'quantity':'multiple'}
	FIELDS['PUBLIC']['VOLUNTEER_POSITION'] = {}
	FIELDS['PUBLIC']['VOLUNTEER_POSITION']['TITLE'] = {'selector':'.item-title', 'type':'text'}
	FIELDS['PUBLIC']['VOLUNTEER_POSITION']['COMPANY'] = {'selector':'.item-subtitle', 'type':'text'}
	FIELDS['PUBLIC']['VOLUNTEER_POSITION']['DATE'] = {'selector':'.date-range', 'type':'text'}
	FIELDS['PUBLIC']['VOLUNTEER_POSITION']['CAUSE'] = {'selector':'.cause', 'type':'text'}
	FIELDS['PUBLIC']['VOLUNTEER_POSITION']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}

	SECTIONS['PUBLIC']['VOLUNTEER_OPPORTUNITIES'] = {'selector':'#volunteering div.opportunities.extra-section li', 'quantity':'multiple'}
	FIELDS['PUBLIC']['VOLUNTEER_OPPORTUNITIES'] = {}
	FIELDS['PUBLIC']['VOLUNTEER_OPPORTUNITIES']['NAME'] = {'selector':'', 'type':'text'}

	SECTIONS['PUBLIC']['VOLUNTEER_CAUSES'] = {'selector':'#volunteering div.extra-section:nth-child(2) > ul:nth-child(2) > li', 'quantity':'multiple'}
	FIELDS['PUBLIC']['VOLUNTEER_CAUSES'] = {}
	FIELDS['PUBLIC']['VOLUNTEER_CAUSES']['NAME'] = {'selector':'', 'type':'text'}

	SECTIONS['PUBLIC']['VOLUNTEER_SUPPORT'] = {'selector':'#volunteering div.extra-section:nth-child(3) > ul:nth-child(2) > li', 'quantity':'multiple'}
	FIELDS['PUBLIC']['VOLUNTEER_SUPPORT'] = {}
	FIELDS['PUBLIC']['VOLUNTEER_SUPPORT']['NAME'] = {'selector':'', 'type':'text'}

	SECTIONS['PUBLIC']['PUBLICATIONS'] = {'selector':'.publication', 'quantity':'multiple'}
	FIELDS['PUBLIC']['PUBLICATIONS'] = {}
	FIELDS['PUBLIC']['PUBLICATIONS']['NAME'] = {'selector':'.item-title', 'type':'text'}
	FIELDS['PUBLIC']['PUBLICATIONS']['URL'] = {'selector':'.item-title a', 'type':'attr', 'attr':'href'}
	FIELDS['PUBLIC']['PUBLICATIONS']['PLACE'] = {'selector':'.item-subtitle', 'type':'text'}
	FIELDS['PUBLIC']['PUBLICATIONS']['DATE'] = {'selector':'.date-range', 'type':'text'}
	FIELDS['PUBLIC']['PUBLICATIONS']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}
	FIELDS['PUBLIC']['PUBLICATIONS']['CONTRIBUTORS'] = {'selector':'.contributors', 'type':'text'}

	SECTIONS['PUBLIC']['COURSES'] = {'selector':'.course', 'quantity':'multiple'}
	FIELDS['PUBLIC']['COURSES'] = {}
	FIELDS['PUBLIC']['COURSES']['NAME'] = {'selector':'', 'type':'text'}

	SECTIONS['PUBLIC']['PROJECTS'] = {'selector':'.project', 'quantity':'multiple'}
	FIELDS['PUBLIC']['PROJECTS'] = {}
	FIELDS['PUBLIC']['PROJECTS']['NAME'] = {'selector':'.item-title', 'type':'text'}	
	FIELDS['PUBLIC']['PROJECTS']['URL'] = {'selector':'.item-title a', 'type':'attr', 'attr':'href'}
	FIELDS['PUBLIC']['PROJECTS']['DATE'] = {'selector':'.date-range', 'type':'text'}
	FIELDS['PUBLIC']['PROJECTS']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}
	FIELDS['PUBLIC']['PROJECTS']['CONTRIBUTORS'] = {'selector':'.contributors', 'type':'text'}	

	SECTIONS['PUBLIC']['AWARDS'] = {'selector':'.award', 'quantity':'multiple'}
	FIELDS['PUBLIC']['AWARDS'] = {}
	FIELDS['PUBLIC']['AWARDS']['NAME'] = {'selector':'.item-title', 'type':'text'}	
	FIELDS['PUBLIC']['AWARDS']['COMPANY'] = {'selector':'.item-subtitle', 'type':'text'}
	FIELDS['PUBLIC']['AWARDS']['DATE'] = {'selector':'.date-range', 'type':'text'}
	FIELDS['PUBLIC']['AWARDS']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}

	SECTIONS['PUBLIC']['LANGUAGES'] = {'selector':'.language', 'quantity':'multiple'}
	FIELDS['PUBLIC']['LANGUAGES'] = {}
	FIELDS['PUBLIC']['LANGUAGES']['NAME'] = {'selector':'.name', 'type':'text'}	
	FIELDS['PUBLIC']['LANGUAGES']['LEVEL'] = {'selector':'.proficiency', 'type':'text'}

	SECTIONS['PUBLIC']['SKILLS'] = {'selector':'.skill', 'quantity':'multiple'}
	FIELDS['PUBLIC']['SKILLS'] = {}
	FIELDS['PUBLIC']['SKILLS']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['PUBLIC']['SKILLS']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['PUBLIC']['EDUCATION'] = {'selector':'.school', 'quantity':'multiple'}
	FIELDS['PUBLIC']['EDUCATION'] = {}
	FIELDS['PUBLIC']['EDUCATION']['NAME'] = {'selector':'.item-title', 'type':'text'}	
	FIELDS['PUBLIC']['EDUCATION']['URL'] = {'selector':'.item-title a', 'type':'attr', 'attr':'href'}
	FIELDS['PUBLIC']['EDUCATION']['DEGREE'] = {'selector':'.item-subtitle', 'type':'text'}
	FIELDS['PUBLIC']['EDUCATION']['DATE'] = {'selector':'.date-range', 'type':'text'}
	FIELDS['PUBLIC']['EDUCATION']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}
	FIELDS['PUBLIC']['EDUCATION']['IMG'] = {'selector':'img', 'type':'attr', 'attr':'src'}

	SECTIONS['PUBLIC']['INTERESTS'] = {'selector':'.interest', 'quantity':'multiple'}
	FIELDS['PUBLIC']['INTERESTS'] = {}
	FIELDS['PUBLIC']['INTERESTS']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['PUBLIC']['INTERESTS']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['PUBLIC']['CERTIFICATIONS'] = {'selector':'.certification', 'quantity':'multiple'}
	FIELDS['PUBLIC']['CERTIFICATIONS'] = {}
	FIELDS['PUBLIC']['CERTIFICATIONS']['NAME'] = {'selector':'.item-title', 'type':'text'}	
	FIELDS['PUBLIC']['CERTIFICATIONS']['URL'] = {'selector':'.item-title a', 'type':'attr', 'attr':'href'}
	FIELDS['PUBLIC']['CERTIFICATIONS']['DEGREE'] = {'selector':'.item-subtitle', 'type':'text'}
	FIELDS['PUBLIC']['CERTIFICATIONS']['DATE'] = {'selector':'.date-range', 'type':'text'}
	FIELDS['PUBLIC']['CERTIFICATIONS']['IMG'] = {'selector':'.logo img', 'type':'attr', 'attr':'src'}

	SECTIONS['PUBLIC']['ORGANIZATIONS'] = {'selector':'#organizations li', 'quantity':'multiple'}
	FIELDS['PUBLIC']['ORGANIZATIONS'] = {}
	FIELDS['PUBLIC']['ORGANIZATIONS']['NAME'] = {'selector':'.item-title', 'type':'text'}	
	FIELDS['PUBLIC']['ORGANIZATIONS']['URL'] = {'selector':'.item-title a', 'type':'attr', 'attr':'href'}
	FIELDS['PUBLIC']['ORGANIZATIONS']['DEGREE'] = {'selector':'.item-subtitle', 'type':'text'}
	FIELDS['PUBLIC']['ORGANIZATIONS']['DATE'] = {'selector':'.date-range', 'type':'text'}

	SECTIONS['PUBLIC']['PATENTS'] = {'selector':'.patent', 'quantity':'multiple'}
	FIELDS['PUBLIC']['PATENTS'] = {}
	FIELDS['PUBLIC']['PATENTS']['NAME'] = {'selector':'.item-title', 'type':'text'}	
	FIELDS['PUBLIC']['PATENTS']['URL'] = {'selector':'.item-title a', 'type':'attr', 'attr':'href'}
	FIELDS['PUBLIC']['PATENTS']['PLACE'] = {'selector':'.item-subtitle', 'type':'text'}
	FIELDS['PUBLIC']['PATENTS']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}
	FIELDS['PUBLIC']['PATENTS']['CONTRIBUTORS'] = {'selector':'.contributors', 'type':'text'}	

	SECTIONS['PUBLIC']['SCORES'] = {'selector':'.score', 'quantity':'multiple'}
	FIELDS['PUBLIC']['SCORES'] = {}
	FIELDS['PUBLIC']['SCORES']['NAME'] = {'selector':'.item-title', 'type':'text'}	
	FIELDS['PUBLIC']['SCORES']['VALUE'] = {'selector':'.item-subtitle', 'type':'text'}
	FIELDS['PUBLIC']['SCORES']['DATE'] = {'selector':'.date-range', 'type':'text'}
	FIELDS['PUBLIC']['SCORES']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}

	SECTIONS['PUBLIC']['RECOMENDATIONS'] = {'selector':'.recommendation', 'quantity':'multiple'}
	FIELDS['PUBLIC']['RECOMENDATIONS'] = {}
	FIELDS['PUBLIC']['RECOMENDATIONS']['NAME'] = {'selector':'', 'type':'text'}	

	SECTIONS['PUBLIC']['GROUPS'] = {'selector':'.group', 'quantity':'multiple'}
	FIELDS['PUBLIC']['GROUPS'] = {}
	FIELDS['PUBLIC']['GROUPS']['NAME'] = {'selector':'.item-title', 'type':'text'}	
	FIELDS['PUBLIC']['GROUPS']['URL'] = {'selector':'.item-title a', 'type':'attr', 'attr':'href'}
	FIELDS['PUBLIC']['GROUPS']['IMG'] = {'selector':'.logo img', 'type':'attr', 'attr':'src'}

	SECTIONS['PUBLIC']['RELATED'] = {'selector':'.profile-card', 'quantity':'multiple'}
	FIELDS['PUBLIC']['RELATED'] = {}
	FIELDS['PUBLIC']['RELATED']['NAME'] = {'selector':'.item-title', 'type':'text'}	
	FIELDS['PUBLIC']['RELATED']['URL'] = {'selector':'.item-title a', 'type':'attr', 'attr':'href'}
	FIELDS['PUBLIC']['RELATED']['VALUE'] = {'selector':'.headline', 'type':'text'}
	FIELDS['PUBLIC']['RELATED']['IMG'] = {'selector':'img', 'type':'attr', 'attr':'src'}

	# LOGGED

	CONTAINER['LOGGED'] = '#profile'
	SECTIONS['LOGGED'] = {}
	FIELDS['LOGGED'] = {}
	SECTIONS['LOGGED']['NAME'] = {'selector':'.full-name', 'type':'text', 'quantity':'single'}
	SECTIONS['LOGGED']['IMAGE'] = {'selector':'.profile-picture img', 'type':'attr', 'attr':'src', 'quantity':'single'}
	SECTIONS['LOGGED']['CONNECTIONS'] = {'selector':'.connections-link,.member-connections', 'type':'text', 'quantity':'single'}
	SECTIONS['LOGGED']['TITLE'] = {'selector':'.title', 'type':'text', 'quantity':'single'}
	SECTIONS['LOGGED']['LOCATION'] = {'selector':'#location .locality', 'type':'text', 'quantity':'single'}
	SECTIONS['LOGGED']['LOCATION_URL'] = {'selector':'#location .locality a', 'type':'attr', 'attr':'href', 'quantity':'single'}
	SECTIONS['LOGGED']['INDUSTRY'] = {'selector':'.industry', 'type':'text', 'quantity':'single'}
	SECTIONS['LOGGED']['INDUSTRY_URL'] = {'selector':'.industry a', 'type':'attr', 'attr':'href', 'quantity':'single'}
	SECTIONS['LOGGED']['RECOMMENDATIONS_NUMBER'] = {'selector':'.nav-received-tab.all-received', 'type':'text', 'quantity':'single'}
	SECTIONS['LOGGED']['SUMMARY'] = {'selector':'.summary', 'type':'text', 'quantity':'single'}
	SECTIONS['LOGGED']['CONTACTS_SHARED'] = {'selector':'.shared', 'type':'text', 'quantity':'single'}
	SECTIONS['LOGGED']['CONTACTS_NEW'] = {'selector':'.new', 'type':'text', 'quantity':'single'}
	SECTIONS['LOGGED']['FRIENDLY_URL'] = {'selector':'.view-public-profile', 'type':'text', 'quantity':'single'}
	SECTIONS['LOGGED']['FOLLOWERS'] = {'selector':'.follow-widget-count', 'type':'text', 'quantity':'single'}
	
	SECTIONS['LOGGED']['BRIEF_CURRENT'] = {'selector':'#overview-summary-current li', 'quantity':'multiple'}
	FIELDS['LOGGED']['BRIEF_CURRENT'] = {}
	FIELDS['LOGGED']['BRIEF_CURRENT']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['LOGGED']['BRIEF_CURRENT']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['LOGGED']['BRIEF_PREVIOUS'] = {'selector':'#overview-summary-past li', 'quantity':'multiple'}
	FIELDS['LOGGED']['BRIEF_PREVIOUS'] = {}
	FIELDS['LOGGED']['BRIEF_PREVIOUS']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['LOGGED']['BRIEF_PREVIOUS']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['LOGGED']['BRIEF_EDUCATION'] = {'selector':'#overview-summary-education li', 'quantity':'multiple'}
	FIELDS['LOGGED']['BRIEF_EDUCATION'] = {}
	FIELDS['LOGGED']['BRIEF_EDUCATION']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['LOGGED']['BRIEF_EDUCATION']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['LOGGED']['EMAILS'] = {'selector':'#email-view li', 'quantity':'multiple'}
	FIELDS['LOGGED']['EMAILS'] = {}
	FIELDS['LOGGED']['EMAILS']['EMAIL'] = {'selector':'', 'type':'text'}
	FIELDS['LOGGED']['EMAILS']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['LOGGED']['IMS'] = {'selector':'#im-view li', 'quantity':'multiple'}
	FIELDS['LOGGED']['IMS'] = {}
	FIELDS['LOGGED']['IMS']['IM'] = {'selector':'', 'type':'text'}

	SECTIONS['LOGGED']['PHONES'] = {'selector':'#phone-view li', 'quantity':'multiple'}
	FIELDS['LOGGED']['PHONES'] = {}
	FIELDS['LOGGED']['PHONES']['PHONE'] = {'selector':'', 'type':'text'}

	SECTIONS['LOGGED']['WEBSITES'] = {'selector':'#website-view li', 'quantity':'multiple'}
	FIELDS['LOGGED']['WEBSITES'] = {}
	FIELDS['LOGGED']['WEBSITES']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['LOGGED']['WEBSITES']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['LOGGED']['TWITTER'] = {'selector':'#twitter-view li', 'quantity':'multiple'}
	FIELDS['LOGGED']['TWITTER'] = {}
	FIELDS['LOGGED']['TWITTER']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['LOGGED']['TWITTER']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['LOGGED']['ATTACHMENTS'] = {'selector':'#summary-item .media-cell', 'quantity':'multiple'}
	FIELDS['LOGGED']['ATTACHMENTS'] = {}
	FIELDS['LOGGED']['ATTACHMENTS']['NAME'] = {'selector':'.description', 'type':'text'}
	FIELDS['LOGGED']['ATTACHMENTS']['IMG'] = {'selector':'img', 'type':'attr', 'attr':'src'}

	SECTIONS['LOGGED']['POSTS'] = {'selector':'.influencer-posts-list > li', 'quantity':'multiple'}
	FIELDS['LOGGED']['POSTS'] = {}
	FIELDS['LOGGED']['POSTS']['NAME'] = {'selector':'.influencer-post-title', 'type':'text'}
	FIELDS['LOGGED']['POSTS']['URL'] = {'selector':'.influencer-post-title a', 'type':'attr', 'attr':'href'}
	FIELDS['LOGGED']['POSTS']['IMG'] = {'selector':'img', 'type':'attr', 'attr':'src'}
	FIELDS['LOGGED']['POSTS']['DATE'] = {'selector':'.influencer-post-published', 'type':'text'}

	SECTIONS['LOGGED']['EXPERIENCE'] = {'selector':'.current-position,past-position', 'quantity':'multiple'}
	FIELDS['LOGGED']['EXPERIENCE'] = {}
	FIELDS['LOGGED']['EXPERIENCE']['TITLE'] = {'selector':'div > header > h4 > a', 'type':'text'}
	FIELDS['LOGGED']['EXPERIENCE']['TITLE_URL'] = {'selector':'div > header > h4 > a', 'type':'attr', 'attr':'href'}
	FIELDS['LOGGED']['EXPERIENCE']['IMG'] = {'selector':'img', 'type':'attr', 'attr':'src'}
	FIELDS['LOGGED']['EXPERIENCE']['COMPANY'] = {'selector':'div > header > h5:nth-child(3) > span > strong > a', 'type':'text'}
	FIELDS['LOGGED']['EXPERIENCE']['COMPANY_URL'] = {'selector':'div > header > h5:nth-child(3) > span > strong > a', 'type':'attr', 'attr':'href'}
	FIELDS['LOGGED']['EXPERIENCE']['DATE'] = {'selector':'.experience-date-locale', 'type':'text'}
	FIELDS['LOGGED']['EXPERIENCE']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}
	
	SECTIONS['LOGGED']['VOLUNTEER_POSITION'] = {'selector':'#background-volunteering > div', 'quantity':'multiple'}
	FIELDS['LOGGED']['VOLUNTEER_POSITION'] = {}
	FIELDS['LOGGED']['VOLUNTEER_POSITION']['TITLE'] = {'selector':'h4', 'type':'text'}
	FIELDS['LOGGED']['VOLUNTEER_POSITION']['COMPANY'] = {'selector':'h5', 'type':'text'}
	FIELDS['LOGGED']['VOLUNTEER_POSITION']['DATE'] = {'selector':'.volunteering-date-cause time', 'type':'text'}
	FIELDS['LOGGED']['VOLUNTEER_POSITION']['CAUSE'] = {'selector':'.locality', 'type':'text'}
	FIELDS['LOGGED']['VOLUNTEER_POSITION']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}

	SECTIONS['LOGGED']['VOLUNTEER_OPPORTUNITIES'] = {'selector':'.volunteering-opportunities > li', 'quantity':'multiple'}
	FIELDS['LOGGED']['VOLUNTEER_OPPORTUNITIES'] = {}
	FIELDS['LOGGED']['VOLUNTEER_OPPORTUNITIES']['NAME'] = {'selector':'', 'type':'text'}

	SECTIONS['LOGGED']['VOLUNTEER_CAUSES'] = {'selector':'.interests .volunteering-listing > li', 'quantity':'multiple'}
	FIELDS['LOGGED']['VOLUNTEER_CAUSES'] = {}
	FIELDS['LOGGED']['VOLUNTEER_CAUSES']['NAME'] = {'selector':'', 'type':'text'}

	SECTIONS['LOGGED']['VOLUNTEER_SUPPORT'] = {'selector':'.non-profits .volunteering-listing > li', 'quantity':'multiple'}
	FIELDS['LOGGED']['VOLUNTEER_SUPPORT'] = {}
	FIELDS['LOGGED']['VOLUNTEER_SUPPORT']['NAME'] = {'selector':'', 'type':'text'}
	FIELDS['LOGGED']['VOLUNTEER_SUPPORT']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['LOGGED']['PUBLICATIONS'] = {'selector':'#background-publications > div', 'quantity':'multiple'}
	FIELDS['LOGGED']['PUBLICATIONS'] = {}
	FIELDS['LOGGED']['PUBLICATIONS']['NAME'] = {'selector':'h4', 'type':'text'}
	FIELDS['LOGGED']['PUBLICATIONS']['URL'] = {'selector':'h4 a', 'type':'attr', 'attr':'href'}
	FIELDS['LOGGED']['PUBLICATIONS']['PLACE'] = {'selector':'h5', 'type':'text'}
	FIELDS['LOGGED']['PUBLICATIONS']['DATE'] = {'selector':'.publication-date', 'type':'text'}
	FIELDS['LOGGED']['PUBLICATIONS']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}
	FIELDS['LOGGED']['PUBLICATIONS']['CONTRIBUTORS'] = {'selector':'.contributors', 'type':'text'}

	SECTIONS['LOGGED']['COURSES'] = {'selector':'.courses-listing > li', 'quantity':'multiple'}
	FIELDS['LOGGED']['COURSES'] = {}
	FIELDS['LOGGED']['COURSES']['NAME'] = {'selector':'', 'type':'text'}

	SECTIONS['LOGGED']['PROJECTS'] = {'selector':'#background-projects > div', 'quantity':'multiple'}
	FIELDS['LOGGED']['PROJECTS'] = {}
	FIELDS['LOGGED']['PROJECTS']['NAME'] = {'selector':'h4', 'type':'text'}	
	FIELDS['LOGGED']['PROJECTS']['URL'] = {'selector':'h4 a', 'type':'attr', 'attr':'href'}
	FIELDS['LOGGED']['PROJECTS']['DATE'] = {'selector':'.projects-date', 'type':'text'}
	FIELDS['LOGGED']['PROJECTS']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}
	FIELDS['LOGGED']['PROJECTS']['CONTRIBUTORS'] = {'selector':'.associated-list', 'type':'text'}	

	SECTIONS['LOGGED']['AWARDS'] = {'selector':'#background-honors > div', 'quantity':'multiple'}
	FIELDS['LOGGED']['AWARDS'] = {}
	FIELDS['LOGGED']['AWARDS']['NAME'] = {'selector':'h4', 'type':'text'}	
	FIELDS['LOGGED']['AWARDS']['COMPANY'] = {'selector':'h5', 'type':'text'}
	FIELDS['LOGGED']['AWARDS']['DATE'] = {'selector':'.honors-date', 'type':'text'}
	FIELDS['LOGGED']['AWARDS']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}

	SECTIONS['LOGGED']['LANGUAGES'] = {'selector':'#languages-view > ol > li', 'quantity':'multiple'}
	FIELDS['LOGGED']['LANGUAGES'] = {}
	FIELDS['LOGGED']['LANGUAGES']['NAME'] = {'selector':'h4', 'type':'text'}	
	FIELDS['LOGGED']['LANGUAGES']['LEVEL'] = {'selector':'.languages-proficiency', 'type':'text'}

	SECTIONS['LOGGED']['SKILLS'] = {'selector':'.skills-section > li', 'quantity':'multiple'}
	FIELDS['LOGGED']['SKILLS'] = {}
	FIELDS['LOGGED']['SKILLS']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['LOGGED']['SKILLS']['ENDORSEMENTS'] = {'selector':'.num-endorsements', 'type':'text'}
	FIELDS['LOGGED']['SKILLS']['NUMBER'] = {'selector':'.endorse-item-name-text', 'type':'text'}
	FIELDS['LOGGED']['SKILLS']['URL'] = {'selector':'.endorse-item-name-text', 'type':'attr', 'attr':'href'}

	SECTIONS['LOGGED']['EDUCATION'] = {'selector':'#background-education > div', 'quantity':'multiple'}
	FIELDS['LOGGED']['EDUCATION'] = {}
	FIELDS['LOGGED']['EDUCATION']['NAME'] = {'selector':'div > div > header > h4 > a', 'type':'text'}	
	FIELDS['LOGGED']['EDUCATION']['URL'] = {'selector':'div > div > header > h4 > a', 'type':'attr', 'attr':'href'}
	FIELDS['LOGGED']['EDUCATION']['DEGREE'] = {'selector':'.degree', 'type':'text'}
	FIELDS['LOGGED']['EDUCATION']['MAJOR'] = {'selector':'.major', 'type':'text'}
	FIELDS['LOGGED']['EDUCATION']['GRADE'] = {'selector':'.grade', 'type':'text'}
	FIELDS['LOGGED']['EDUCATION']['DATE'] = {'selector':'.education-date', 'type':'text'}
	FIELDS['LOGGED']['EDUCATION']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}
	FIELDS['LOGGED']['EDUCATION']['NOTES'] = {'selector':'.notes', 'type':'text'}
	FIELDS['LOGGED']['EDUCATION']['IMG'] = {'selector':'.education-logo img', 'type':'attr', 'attr':'src'}

	SECTIONS['LOGGED']['INTERESTS'] = {'selector':'.interests-listing > li', 'quantity':'multiple'}
	FIELDS['LOGGED']['INTERESTS'] = {}
	FIELDS['LOGGED']['INTERESTS']['NAME'] = {'selector':'a', 'type':'text'}
	FIELDS['LOGGED']['INTERESTS']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}

	SECTIONS['LOGGED']['CERTIFICATIONS'] = {'selector':'#background-certifications div', 'quantity':'multiple'}
	FIELDS['LOGGED']['CERTIFICATIONS'] = {}
	FIELDS['LOGGED']['CERTIFICATIONS']['NAME'] = {'selector':'h4', 'type':'text'}	
	FIELDS['LOGGED']['CERTIFICATIONS']['URL'] = {'selector':'h4 a', 'type':'attr', 'attr':'href'}
	FIELDS['LOGGED']['CERTIFICATIONS']['DEGREE'] = {'selector':'h5', 'type':'text'}
	FIELDS['LOGGED']['CERTIFICATIONS']['DATE'] = {'selector':'.certification-date', 'type':'text'}
	FIELDS['LOGGED']['CERTIFICATIONS']['IMG'] = {'selector':'img', 'type':'attr', 'attr':'src'}

	SECTIONS['LOGGED']['ORGANIZATIONS'] = {'selector':'#background-organizations div', 'quantity':'multiple'}
	FIELDS['LOGGED']['ORGANIZATIONS'] = {}
	FIELDS['LOGGED']['ORGANIZATIONS']['NAME'] = {'selector':'h4', 'type':'text'}	
	FIELDS['LOGGED']['ORGANIZATIONS']['URL'] = {'selector':'h4 a', 'type':'attr', 'attr':'href'}
	FIELDS['LOGGED']['ORGANIZATIONS']['DEGREE'] = {'selector':'h5', 'type':'text'}
	FIELDS['LOGGED']['ORGANIZATIONS']['DATE'] = {'selector':'.organizations-date', 'type':'text'}

	SECTIONS['LOGGED']['PATENTS'] = {'selector':'#background-patents > div', 'quantity':'multiple'}
	FIELDS['LOGGED']['PATENTS'] = {}
	FIELDS['LOGGED']['PATENTS']['NAME'] = {'selector':'h4', 'type':'text'}	
	FIELDS['LOGGED']['PATENTS']['PLACE'] = {'selector':'h5', 'type':'text'}
	FIELDS['LOGGED']['PATENTS']['DATE'] = {'selector':'.patents-date', 'type':'text'}

	SECTIONS['LOGGED']['SCORES'] = {'selector':'#background-test-scores > div', 'quantity':'multiple'}
	FIELDS['LOGGED']['SCORES'] = {}
	FIELDS['LOGGED']['SCORES']['NAME'] = {'selector':'h4', 'type':'text'}	
	FIELDS['LOGGED']['SCORES']['VALUE'] = {'selector':'h5', 'type':'text'}
	FIELDS['LOGGED']['SCORES']['DATE'] = {'selector':'.test-scores-date', 'type':'text'}

	SECTIONS['LOGGED']['RECOMENDATIONS_RECEIVED'] = {'selector':'.endorsements-received li', 'quantity':'multiple'}
	FIELDS['LOGGED']['RECOMENDATIONS_RECEIVED'] = {}
	FIELDS['LOGGED']['RECOMENDATIONS_RECEIVED']['POSITION'] = {'selector':'h3', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_RECEIVED']['PLACE'] = {'selector':'h4', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_RECEIVED']['PERSON'] = {'selector':'h5', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_RECEIVED']['PROFILE'] = {'selector':'h5 a', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_RECEIVED']['JOB'] = {'selector':'h6', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_RECEIVED']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_RECEIVED']['DATE'] = {'selector':'.endorsement-date', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_RECEIVED']['IMAGE'] = {'selector':'.endorsement-picture img', 'type':'attr', 'attr':'src'}	
	FIELDS['LOGGED']['RECOMENDATIONS_RECEIVED']['URL'] = {'selector':'.endorsement-picture a', 'type':'attr', 'attr':'href'}	

	SECTIONS['LOGGED']['RECOMENDATIONS_GIVEN'] = {'selector':'.endorsements-given li', 'quantity':'multiple'}
	FIELDS['LOGGED']['RECOMENDATIONS_GIVEN'] = {}
	FIELDS['LOGGED']['RECOMENDATIONS_GIVEN']['NAME'] = {'selector':'', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_GIVEN']['POSITION'] = {'selector':'h3', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_GIVEN']['PLACE'] = {'selector':'h4', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_GIVEN']['PERSON'] = {'selector':'h5', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_GIVEN']['PROFILE'] = {'selector':'h5 a', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_GIVEN']['JOB'] = {'selector':'h6', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_GIVEN']['DESCRIPTION'] = {'selector':'.description', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_GIVEN']['DATE'] = {'selector':'.endorsement-date', 'type':'text'}	
	FIELDS['LOGGED']['RECOMENDATIONS_GIVEN']['IMAGE'] = {'selector':'.endorsement-picture img', 'type':'attr', 'attr':'src'}	
	FIELDS['LOGGED']['RECOMENDATIONS_GIVEN']['URL'] = {'selector':'.endorsement-picture a', 'type':'attr', 'attr':'href'}

	SECTIONS['LOGGED']['GROUPS'] = {'selector':'.groups-container li', 'quantity':'multiple'}
	FIELDS['LOGGED']['GROUPS'] = {}
	FIELDS['LOGGED']['GROUPS']['NAME'] = {'selector':'.group-link', 'type':'text'}	
	FIELDS['LOGGED']['GROUPS']['URL'] = {'selector':'.group-link', 'type':'attr', 'attr':'href'}
	FIELDS['LOGGED']['GROUPS']['MEMBERS'] = {'selector':'.groups-stats', 'type':'text'}	
	FIELDS['LOGGED']['GROUPS']['IMG'] = {'selector':'img', 'type':'attr', 'attr':'src'}

	SECTIONS['LOGGED']['RELATED'] = {'selector':'.discovery-results li', 'quantity':'multiple'}
	FIELDS['LOGGED']['RELATED'] = {}
	FIELDS['LOGGED']['RELATED']['NAME'] = {'selector':'img', 'type':'attr', 'attr':'alt'}
	FIELDS['LOGGED']['RELATED']['URL'] = {'selector':'a', 'type':'attr', 'attr':'href'}
	FIELDS['LOGGED']['RELATED']['IMG'] = {'selector':'img', 'type':'attr', 'attr':'src'}
	FIELDS['LOGGED']['RELATED']['LEVEL'] = {'selector':'.degree-icon', 'type':'text'}	

	SECTIONS['LOGGED']['SIMILAR'] = {'selector':'.browse-map-list li', 'quantity':'multiple'}
	FIELDS['LOGGED']['SIMILAR'] = {}
	FIELDS['LOGGED']['SIMILAR']['NAME'] = {'selector':'h4', 'type':'text'}	
	FIELDS['LOGGED']['SIMILAR']['URL'] = {'selector':'h4 a', 'type':'attr', 'attr':'href'}
	FIELDS['LOGGED']['SIMILAR']['IMG'] = {'selector':'img', 'type':'attr', 'attr':'src'}
	FIELDS['LOGGED']['SIMILAR']['TITLE'] = {'selector':'.browse-map-title', 'type':'text'}	

	SECTIONS['LOGGED']['FOLLOWING'] = {'selector':'.following-container > li', 'quantity':'multiple'}
	FIELDS['LOGGED']['FOLLOWING'] = {}
	FIELDS['LOGGED']['FOLLOWING']['NAME'] = {'selector':'.channel-name a,following-name a', 'type':'text'}	
	FIELDS['LOGGED']['FOLLOWING']['URL'] = {'selector':'.channel-name a,following-name a', 'type':'attr', 'attr':'href'}
	FIELDS['LOGGED']['FOLLOWING']['DETAILS'] = {'selector':'.following-stats,.following-name', 'type':'text'}	
	FIELDS['LOGGED']['FOLLOWING']['IMG'] = {'selector':'img', 'type':'attr', 'attr':'src'}

	SECTIONS['LOGGED']['PERSONAL'] = {'selector':'#personal-info-view', 'quantity':'multiple'}
	FIELDS['LOGGED']['PERSONAL'] = {}
	FIELDS['LOGGED']['PERSONAL']['EXTRA'] = {'selector':'', 'type':'text'}

	sel = None

	def __init__(self, params=None):
		if self.MODE == 'LOGGED':
			self.sel = LinkedinHelper.get_logged_in_driver(params)
		else:
			self.sel = LinkedinHelper.get_driver(params)

	def run(self, params, callback=None, bulk=False):
		urls = params['added']
		mode = params['mode'] if 'mode' in params else self.MODE
		if bulk:
			profiles = []
		for url in urls:
			self.sel.loadAndWait(url, self.CONTAINER[mode])
			self.sel.clickSelector('#contact-info-tab')
			self.sel.clickMultiple('.hidden-view-more')
			self.sel.clickMultiple('.toggle-show-more')
			self.sel.clickMultiple('.see-action')
			self.sel.clickMultiple('.see-more-less')
			if mode == 'LOGGED':
				self.sel.clickMultiple('.see-more')
			else:
				self.sel.clickMultiple('li.see-more label')
				self.sel.clickMultiple('.recommendation label')
			time.sleep(0.3)
			data = self.sel.extractSectionFromObjects(mode, self.SECTIONS, self.FIELDS)
			data['userUrl'] = url
			data['friendlyUrl'] = self.sel.getUrl()
			data['connId'] = LinkedinHelper.get_conn_id(self.sel.getCode())
			if callback:
				callback(data)
			if bulk:
				profiles.append(data)
		self.sel.close()
		if bulk:
			return profiles
