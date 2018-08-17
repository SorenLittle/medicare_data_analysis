import numpy as np
import datetime as dt
import pandas as pd
from sodapy import Socrata

client = Socrata("data.medicare.gov", None)


def main():
    # THIS LINES USE THE SOCRATA CLIENT TO GET THE MEDICARE DATA
    # providers_df = get_dataframe("b27b-2uc7", 1000)  # ALL ROWS = 15616
    # surveys_df = get_dataframe("gx3u-faec", 1000)  # ALL ROWS = 46450
    # deficiencies_health_df = get_dataframe("ikq5-jt9b", 1000)  # ALL ROWS = 346030
    # deficiencies_fire_df = get_dataframe("emvx-vqfd", 1000)  # ALL ROWS = 145438
    # penalties_df = get_dataframe("im9k-ugyp", 1000)  # ALL ROWS = 8258
    # owners_df = get_dataframe("eaa9-qkxm", 1000)  # ALL ROWS = 172959

    # THIS FUNCTION PRODUCES A DF OF ALL THE PROVIDERS AND THEIR INFORMATION
    # providers_df = clean_providers(providers_df)

    # THESE THREE FUNCTIONS PRODUCE A DF WITH ALL DEFICIENCIES LINKED TO SURVEYS BY INDEX
    # surveys_df = clean_surveys(surveys_df)
    # deficiencies_df = clean_deficiencies(deficiencies_health_df, deficiencies_fire_df)
    # deficiencies_df = merge_deficiencies_and_surveys(deficiencies_df, surveys_df)

    # THIS FUNCTION PRODUCES A DF OF ALL THE PENALTIES ISSUED
    # penalties_df = clean_penalties(penalties_df)

    # THIS FUNCTION PRODUCES A CLEAN LIST OF OWNERS
    # owners_df = clean_owners(owners_df)

    pass


def clean_providers(df):
    providers_df = df.loc[:, ['federal_provider_number',
                              'legal_business_name',
                              'location_address',
                              'location_city',
                              'location_state',
                              'location_zip',
                              'number_of_certified_beds']]

    return providers_df


def clean_surveys(df):
    surveys_df = df.loc[:, ['federal_provider_number', 'health_survey_date', 'fire_saftey_survey_date']]
    surveys_df['health_survey_date'] = pd.to_datetime(surveys_df['health_survey_date'])
    surveys_df['fire_saftey_survey_date'] = pd.to_datetime(surveys_df['fire_saftey_survey_date'])
    surveys_df.rename(columns={'fire_saftey_survey_date': 'fire_safety_survey_date'}, inplace=True)

    return surveys_df


def clean_deficiencies(health_df, fire_df):
    temp_health_df = health_df.loc[:, ['federal_provider_number',
                                       'survey_date',
                                       'complaint_deficiency',
                                       'deficiency_corrected',
                                       'correction_date',
                                       'deficiency_description',
                                       'deficiency_prefix',
                                       'deficiency_tag_number',
                                       'health_inspection_on_or_after_11_28_2017',
                                       'inspection_cycle',
                                       'scope_severity_code',
                                       'survey_type']]

    temp_health_df['survey_date'] = pd.to_datetime(temp_health_df['survey_date'])
    temp_health_df['correction_date'] = pd.to_datetime(temp_health_df['correction_date'])

    temp_health_df['compliance_effective'] = np.where(temp_health_df['health_inspection_on_or_after_11_28_2017'] == 'Y',
                                                      True, False)
    temp_health_df = temp_health_df.drop(columns='health_inspection_on_or_after_11_28_2017')

    # print(temp_health_df.head().to_string())
    # print(temp_health_df.info())

    temp_fire_df = fire_df.loc[:, ['federal_provider_number',
                                   'survey_date',
                                   'complaint_deficiency',
                                   'deficiency_corrected',
                                   'correction_date',
                                   'deficiency_description',
                                   'deficiency_prefix',
                                   'deficiency_tag_number',
                                   'tag_version',
                                   'inspection_cycle',
                                   'scope_severity_code',
                                   'survey_type']]

    temp_fire_df['survey_date'] = pd.to_datetime(temp_fire_df['survey_date'])
    temp_fire_df['correction_date'] = pd.to_datetime(temp_fire_df['correction_date'])

    temp_fire_df['compliance_effective'] = np.where(temp_fire_df['tag_version'] == 'New', True, False)
    temp_fire_df = temp_fire_df.drop(columns='tag_version')

    # print(temp_fire_df.to_string())
    # print(temp_fire_df.info())

    frames = [temp_health_df, temp_fire_df]
    deficiencies_df = pd.concat(frames, ignore_index=True)

    return deficiencies_df


def merge_deficiencies_and_surveys(deficiencies_df, surveys_df):
    # HAVE TO CONVERT DATES TO NUMERIC BEFORE SPLITTING THE DATAFRAME
    temp_surveys_df = surveys_df

    surveys_health_df = temp_surveys_df.drop(columns='fire_safety_survey_date')
    surveys_fire_df = temp_surveys_df.drop(columns='health_survey_date')
    surveys_fire_df = surveys_fire_df.dropna()
    # print(surveys_fire_df)

    surveys_health_df['health_survey_date'] = surveys_health_df['health_survey_date'].apply(
        lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
    surveys_fire_df['fire_safety_survey_date'] = surveys_fire_df['fire_safety_survey_date'].apply(
        lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))

    surveys_health_df['combo_code'] = 'Health' + ', ' + surveys_health_df['federal_provider_number'] + ', ' + \
                                      surveys_health_df['health_survey_date']

    surveys_fire_df['combo_code'] = 'Fire Safety' + ', ' + surveys_fire_df['federal_provider_number'] + ', ' + \
                                    surveys_fire_df['fire_safety_survey_date']

    # print(surveys_fire_df)
    # print(surveys_health_df)
    frames = [surveys_health_df, surveys_fire_df]
    survey_combo_codes = pd.concat(frames, sort=True)
    survey_combo_codes = survey_combo_codes.drop(
        columns=['federal_provider_number', 'fire_safety_survey_date', 'health_survey_date'])
    survey_combo_codes['survey_id'] = survey_combo_codes.index

    # print(survey_combo_codes.to_string())

    temp_deficiencies_df = deficiencies_df
    temp_deficiencies_df['survey_date'] = temp_deficiencies_df['survey_date'].apply(
        lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
    temp_deficiencies_df['combo_code'] = temp_deficiencies_df['survey_type'] + ', ' + temp_deficiencies_df[
        'federal_provider_number'] + ', ' + temp_deficiencies_df['survey_date']

    # print(temp_deficiencies_df.to_string())

    # deficiencies_with_surveys_df = pd.merge(temp_deficiencies_df, survey_combo_codes)
    deficiencies_with_surveys_df = temp_deficiencies_df.merge(survey_combo_codes, how='left')
    # print(deficiencies_with_surveys_df[deficiencies_with_surveys_df.isnull().any(axis=1)].head(30).to_string())
    # print(deficiencies_with_surveys_df.to_string())

    deficiencies_with_surveys_df = deficiencies_with_surveys_df.drop(columns='combo_code')
    deficiencies_with_surveys_df['survey_date'] = pd.to_datetime(deficiencies_with_surveys_df['survey_date'])
    # print(deficiencies_with_surveys_df.info())

    return deficiencies_with_surveys_df


def clean_penalties(df):
    penalties_df = df.loc[:, ['penalty_type',
                              'penalty_date',
                              'fine_amount',
                              'federal_provider_number',
                              'payment_denial_start_date',
                              'payment_denial_length_in_days']]

    penalties_df['payment_denial_start_date'] = pd.to_datetime(penalties_df['payment_denial_start_date'])

    return penalties_df


def clean_owners(df):
    owners_df = df.loc[:, ['owner_name',
                           'owner_type',
                           'federal_provider_number',
                           'role_description',
                           'ownership_percentage',
                           'association_date',
                           'location_address',
                           'location_city',
                           'location_state',
                           'location_zip']]

    # owners_df['association_date'] = owners_df['association_date'].map(lambda x: str(x).lstrip('since'))
    # owners_df['association_date'] = pd.to_datetime(owners_df['association_date'], format='%m/%d/%Y', exact=False)
    owners_df = owners_df[pd.notnull(owners_df['owner_name'])]
    owners_df = owners_df.rename(columns={'role_description': 'role'})

    return owners_df


def print_info(selection, df):
    if selection == 'providers':
        print("---------------------------------------------------------------------")
        print("                          PROVIDERS INFO")
        print("---------------------------------------------------------------------")
        print(df.info())
        print()
    if selection == 'surveys':
        print("---------------------------------------------------------------------")
        print("                           SURVEYS INFO")
        print("---------------------------------------------------------------------")
        print(df.info())
        print()
    if selection == 'health deficiencies':
        print("---------------------------------------------------------------------")
        print("                     HEALTH DEFICIENCIES INFO")
        print("---------------------------------------------------------------------")
        print(df.info())
        print()
    if selection == 'fire deficiencies':
        print("---------------------------------------------------------------------")
        print("                      FIRE DEFICIENCIES INFO")
        print("---------------------------------------------------------------------")
        print(df.info())
        print()
    if selection == 'penalties':
        print("---------------------------------------------------------------------")
        print("                           PENALTIES INFO")
        print("---------------------------------------------------------------------")
        print(df.info())
        print()
    if selection == 'owners':
        print("---------------------------------------------------------------------")
        print("                            OWNERS INFO:")
        print("---------------------------------------------------------------------")
        print(df.info())
        print()


def get_dataframe(extension, number):
    # resp = requests.get(url + 'gx3u-faec.json')
    # print(resp.text)

    # if resp.status_code != 200:
    #     print('Error accessing data: {} {}'.format(resp.status_code, resp.text))

    # PRODUCES PANDAS DATAFRAME FROM API
    # CODE FOR API FETCHING FOUND HERE: https://dev.socrata.com/foundry/data.medicare.gov/gx3u-faec
    # UNDER 'CODE SNIPPETS'

    print('Getting {} values from {}...'.format(number, extension))
    resp = client.get(extension, limit=number)

    return pd.DataFrame.from_records(resp)


if __name__ == '__main__':
    main()
