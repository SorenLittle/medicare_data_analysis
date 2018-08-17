import numpy as np
import os
from datetime import datetime
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import getting_json as get


# providers_df = get.get_dataframe("b27b-2uc7", 1000)  # ALL ROWS = 15616
# surveys_df = get.get_dataframe("gx3u-faec", 1000)  # ALL ROWS = 46450
# deficiencies_health_df = get.get_dataframe("ikq5-jt9b", 1000)  # ALL ROWS = 346030
# deficiencies_fire_df = get.get_dataframe("emvx-vqfd", 1000)  # ALL ROWS = 145438
# penalties_df = get.get_dataframe("im9k-ugyp", 1000)  # ALL ROWS = 8258
# owners_df = get.get_dataframe("eaa9-qkxm", 1000)  # ALL ROWS = 172959


def main():
    selection = user_interface()

    while selection:
        if selection == '3':
            # THIS FUNCTION PRODUCES A DF WITH THE TOTAL NUMBER OF DEFICIENCIES FOR EACH PROVIDER
            df = total_deficiencies_by_facility()
            print()
            print(df.to_string())
            print()

            to_csv = input('CONVERT TO CSV? [y/n]: ')
            if to_csv == 'y':
                date = str(datetime.today())
                name = f'Total_Deficiencies_by_Provider_{date[:10]}.csv'
                path = input('path: ')
                df.to_csv(os.path.join(path, name))
        if selection == '1':
            # THIS FUNCTION PRODUCES A DF WITH THE TOTAL NUMBER OF OCCURRENCES OF EACH SEVERITY LEVEL
            df = total_severity_macro()
            print()
            print(df.to_string())
            print()

            to_csv = input('CONVERT TO CSV? [y/n]: ')
            if to_csv == 'y':
                date = str(datetime.today())
                name = f'Total_Severity_Macro_{date[:10]}.csv'
                path = input('path: ')
                df.to_csv(os.path.join(path, name))
        if selection == '4':
            # THIS FUNCTION PRODUCES A DF WITH THE TOTAL NUMBER OF EACH SEVERITY LEVEL BY PROVIDER
            df = total_severity_by_facility()
            print()
            print(df.to_string())
            print()

            to_csv = input('CONVERT TO CSV? [y/n]: ')
            if to_csv == 'y':
                date = str(datetime.today())
                name = f'Total_Severity_by_Provider_{date[:10]}.csv'
                path = input('path: ')
                df.to_csv(os.path.join(path, name))
        if selection == '2':
            # THIS FUNCTION PRODUCES A DF WITH THE TOTAL NUMBER OF EACH F TAG ALONG WITH THEIR TYPES AND DESCRIPTIONS
            df = total_tags_macro()
            print()
            print(df.to_string())
            print()

            to_csv = input('CONVERT TO CSV? [y/n]: ')
            if to_csv == 'y':
                date = str(datetime.today())
                name = f'Total_F_Tags_Macro_{date[:10]}.csv'
                path = input('path: ')
                df.to_csv(os.path.join(path, name))
        if selection == '5':
            # THIS FUNCTION PRODUCES A DF WITH THE TOTAL NUMBER OF EACH F TAG BY PROVIDER
            df = total_tags_by_facility()
            print()
            print(df.to_string())
            print()

            to_csv = input('CONVERT TO CSV? [y/n]: ')
            if to_csv == 'y':
                date = str(datetime.today())
                name = f'Total_F_Tags_by_Facility_{date[:10]}.csv'
                path = input('path: ')
                df.to_csv(os.path.join(path, name))
        if selection == '7':
            # THIS FUNCTION CHARTS THE NUMBER OF DEFICIENCIES OVER TIME
            chart_deficiencies_number_macro()
        if selection == '8':
            # THIS BLOCK OF CODE WILL TAKE A NAME AND RETURN ALL OF THE DEFICIENCIES THEY ARE RESPONSIBLE FOR
            surveys_df = get.get_dataframe("gx3u-faec", 46450)  # ALL ROWS = 46450
            deficiencies_health_df = get.get_dataframe("ikq5-jt9b", 346030)  # ALL ROWS = 346030
            deficiencies_fire_df = get.get_dataframe("emvx-vqfd", 145438)  # ALL ROWS = 145438

            deficiencies_df = get.merge_deficiencies_and_surveys(
                get.clean_deficiencies(deficiencies_health_df, deficiencies_fire_df), get.clean_surveys(surveys_df))

            owners_df = get.get_dataframe("eaa9-qkxm", 172959)  # ALL ROWS = 172959
            owners_df = get.clean_owners(owners_df)

            provider_list, owner = get_providers_from_owner(owners_df)

            chart_deficiencies_by_owner(deficiencies_df, provider_list, owner)
        if selection == '6':
            # THIS FUNCTION GOES FROM PROVIDER TO OWNERS AND THEN TO PROVIDERS BASED ON INVOLVEMENT
            owners_df = get.get_dataframe("eaa9-qkxm", 172959)  # ALL ROWS = 172959
            owners_df = get.clean_owners(owners_df)

            providers_df = get.get_dataframe("b27b-2uc7", 15616)  # ALL ROWS = 15616
            providers_df = get.clean_providers(providers_df)

            print()
            get_ownership_info(owners_df, providers_df)

        print('--------------------------------------------------------------------------------------------')
        print('                                          COMPLETE                                          ')
        print('--------------------------------------------------------------------------------------------')

        print('WOULD YOU LIKE TO PERFORM ANOTHER ACTION?')
        print()

        print('      macro')
        print('[ 1 ] Total occurrences of each severity level (macro)')
        print('[ 2 ] Total occurrences of each f tag (macro)')
        print()
        print('      by provider')
        print('[ 3 ] Total number of deficiencies by provider')
        print('[ 4 ] Total number of each severity level by provider')
        print('[ 5 ] Total number of each f tag by provider')
        print('[ 6 ] Find all ownership affiliations by provider')
        print()
        print('      charts')
        print('[ 7 ] Chart all deficiencies over time')
        print('[ 8 ] Chart deficiencies by individual/organization')
        print()

        selection = input('SELECTION: ')
        print('working...')

    # THIS FUNCTION WAS USED TO PRODUCE THE CSV DOCUMENTS IN THE 'role_counts_csv' FOLDER
    # owners_df = get.get_dataframe("eaa9-qkxm", 172959)  # ALL ROWS = 172959
    # owners_df = get.clean_owners(owners_df)
    #
    # get_ownership_groups(owners_df)


def user_interface():
    time.sleep(.3)
    print('--------------------------------------------------------------------------------------------')
    print('                                     NURSING HOME DATA')
    print('--------------------------------------------------------------------------------------------')
    print()

    print('PLEASE SELECT AN OPTION FROM THE LIST BELOW')
    print()

    print('      macro')
    print('[ 1 ] Total occurrences of each severity level (macro)')
    print('[ 2 ] Total occurrences of each f tag (macro)')
    print()
    print('      by provider')
    print('[ 3 ] Total number of deficiencies by provider')
    print('[ 4 ] Total number of each severity level by provider')
    print('[ 5 ] Total number of each f tag by provider')
    print('[ 6 ] Find all ownership affiliations by provider')
    print()
    print('      charts')
    print('[ 7 ] Chart all deficiencies over time')
    print('[ 8 ] Chart deficiencies by individual/organization')
    print()

    selection = input('SELECTION: ')
    print('working...')

    print()
    print('--------------------------------------------------------------------------------------------')
    print()

    return selection


def total_deficiencies_by_facility():
    surveys_df = get.get_dataframe("gx3u-faec", 46450)  # ALL ROWS = 46450
    deficiencies_health_df = get.get_dataframe("ikq5-jt9b", 346030)  # ALL ROWS = 346030
    deficiencies_fire_df = get.get_dataframe("emvx-vqfd", 145438)  # ALL ROWS = 145438

    deficiencies_df = get.merge_deficiencies_and_surveys(
        get.clean_deficiencies(deficiencies_health_df, deficiencies_fire_df), get.clean_surveys(surveys_df))

    # print(deficiencies_df.to_string())

    count_series = deficiencies_df['federal_provider_number'].value_counts()
    count_df = count_series.to_frame()
    count_df = count_df.rename(columns={'federal_provider_number': 'deficiencies_count'})
    count_df['federal_provider_number'] = count_df.index
    # print(count_df.info())
    # print(count_df.head(30).to_string())

    providers_df = get.get_dataframe("b27b-2uc7", 15616)  # ALL ROWS = 15616
    providers_df = get.clean_providers(providers_df)

    # print(providers_df.info())
    # print(providers_df.head(50).to_string())

    providers_with_deficiencies_df = providers_df.merge(count_df, how='left')

    # print(providers_with_deficiencies_df.info())
    providers_with_deficiencies_df = providers_with_deficiencies_df.sort_values('deficiencies_count', ascending=False)

    return providers_with_deficiencies_df


def total_severity_macro():
    surveys_df = get.get_dataframe("gx3u-faec", 46450)  # ALL ROWS = 46450
    deficiencies_health_df = get.get_dataframe("ikq5-jt9b", 346030)  # ALL ROWS = 346030
    deficiencies_fire_df = get.get_dataframe("emvx-vqfd", 145438)  # ALL ROWS = 145438

    deficiencies_df = get.merge_deficiencies_and_surveys(
        get.clean_deficiencies(deficiencies_health_df, deficiencies_fire_df), get.clean_surveys(surveys_df))

    # print(deficiencies_df.info())
    # print(deficiencies_df.head(50).to_string())

    count_series = deficiencies_df['scope_severity_code'].value_counts()
    count_df = count_series.to_frame()
    count_df = count_df.rename(columns={'scope_severity_code': 'severity_code_count'})
    count_df['scope_severity_code'] = count_df.index
    count_df = count_df.reset_index(drop=True)
    # print(count_df.info())

    return count_df


def total_severity_by_facility():
    surveys_df = get.get_dataframe("gx3u-faec", 46450)  # ALL ROWS = 46450
    deficiencies_health_df = get.get_dataframe("ikq5-jt9b", 346030)  # ALL ROWS = 346030
    deficiencies_fire_df = get.get_dataframe("emvx-vqfd", 145438)  # ALL ROWS = 145438

    deficiencies_df = get.merge_deficiencies_and_surveys(
        get.clean_deficiencies(deficiencies_health_df, deficiencies_fire_df), get.clean_surveys(surveys_df))

    # print(deficiencies_df.info())
    # print(deficiencies_df.head(50).to_string())

    severity_by_facility = pd.crosstab(deficiencies_df.federal_provider_number, deficiencies_df.scope_severity_code)
    severity_by_facility = severity_by_facility.sort_values('L', ascending=False)
    severity_by_facility['federal_provider_number'] = severity_by_facility.index
    severity_by_facility = severity_by_facility.reset_index(drop=True)

    # print(severity_by_facility.to_string())

    providers_df = get.get_dataframe("b27b-2uc7", 15616)  # ALL ROWS = 15616
    providers_df = get.clean_providers(providers_df)

    providers_with_severity_df = providers_df.merge(severity_by_facility, how='left')
    providers_with_severity_df = providers_with_severity_df.drop(columns=['location_address',
                                                                          'location_city',
                                                                          'location_state',
                                                                          'location_zip',
                                                                          'number_of_certified_beds'])

    providers_with_severity_df = providers_with_severity_df.sort_values('L', ascending=False)
    # providers_with_severity_df.to_csv('providers_with_severity.csv')

    return providers_with_severity_df


def total_tags_macro():
    surveys_df = get.get_dataframe("gx3u-faec", 46450)  # ALL ROWS = 46450
    deficiencies_health_df = get.get_dataframe("ikq5-jt9b", 346030)  # ALL ROWS = 346030
    deficiencies_fire_df = get.get_dataframe("emvx-vqfd", 145438)  # ALL ROWS = 145438

    deficiencies_df = get.merge_deficiencies_and_surveys(
        get.clean_deficiencies(deficiencies_health_df, deficiencies_fire_df), get.clean_surveys(surveys_df))

    temp_deficiencies_df = deficiencies_df
    temp_deficiencies_df['f_tag'] = temp_deficiencies_df['deficiency_prefix'] + temp_deficiencies_df[
        'deficiency_tag_number'].apply(lambda x: x[1:])

    # print(deficiencies_df.info())
    # print(deficiencies_df.head(50).to_string())

    count_series = temp_deficiencies_df['f_tag'].value_counts()
    count_df = count_series.to_frame()
    count_df = count_df.rename(columns={'f_tag': 'f_tag_count'})
    count_df['f_tag'] = count_df.index
    count_df = count_df.reset_index(drop=True)

    # print(count_df.head(50))

    dedupe_deficiencies_df = temp_deficiencies_df.drop_duplicates(['f_tag'])
    dedupe_deficiencies_df = dedupe_deficiencies_df.drop(columns=['federal_provider_number',
                                                                  'survey_date',
                                                                  'complaint_deficiency',
                                                                  'deficiency_corrected',
                                                                  'correction_date',
                                                                  'deficiency_prefix',
                                                                  'deficiency_tag_number',
                                                                  'inspection_cycle',
                                                                  'scope_severity_code',
                                                                  'compliance_effective',
                                                                  'survey_id'])

    # print(dedupe_deficiencies_df.info())
    # print(dedupe_deficiencies_df.head(50).to_string())

    count_df = count_df.merge(dedupe_deficiencies_df, how='left')
    return count_df


def total_tags_by_facility():
    surveys_df = get.get_dataframe("gx3u-faec", 46450)  # ALL ROWS = 46450
    deficiencies_health_df = get.get_dataframe("ikq5-jt9b", 346030)  # ALL ROWS = 346030
    deficiencies_fire_df = get.get_dataframe("emvx-vqfd", 145438)  # ALL ROWS = 145438

    deficiencies_df = get.merge_deficiencies_and_surveys(
        get.clean_deficiencies(deficiencies_health_df, deficiencies_fire_df), get.clean_surveys(surveys_df))

    deficiencies_df['f_tag'] = deficiencies_df['deficiency_prefix'] + deficiencies_df[
        'deficiency_tag_number'].apply(lambda x: x[1:])

    # print(deficiencies_df.info())
    # print(deficiencies_df.head(50).to_string())

    tags_by_facility = pd.crosstab(deficiencies_df.federal_provider_number, deficiencies_df.f_tag)
    # tags_mean_df = tags_by_facility
    tags_by_facility['federal_provider_number'] = tags_by_facility.index
    tags_by_facility = tags_by_facility.reset_index(drop=True)

    # print(tags_by_facility.head(50).to_string())

    providers_df = get.get_dataframe("b27b-2uc7", 15616)  # ALL ROWS = 15616
    providers_df = get.clean_providers(providers_df)

    tags_by_facility = providers_df.merge(tags_by_facility, how='left')
    tags_by_facility = tags_by_facility.drop(columns=['location_address',
                                                      'location_city',
                                                      'location_state',
                                                      'location_zip',
                                                      'number_of_certified_beds'])

    tags_by_facility = tags_by_facility.sort_values('F441', ascending=False)

    return tags_by_facility


def chart_deficiencies_number_macro():
    surveys_df = get.get_dataframe("gx3u-faec", 46450)  # ALL ROWS = 46450
    deficiencies_health_df = get.get_dataframe("ikq5-jt9b", 346030)  # ALL ROWS = 346030
    deficiencies_fire_df = get.get_dataframe("emvx-vqfd", 145438)  # ALL ROWS = 145438

    deficiencies_df = get.merge_deficiencies_and_surveys(
        get.clean_deficiencies(deficiencies_health_df, deficiencies_fire_df), get.clean_surveys(surveys_df))

    # print(deficiencies_df.info())
    # print(deficiencies_df.head(50).to_string())

    count_series = deficiencies_df['survey_date'].value_counts()
    count_df = count_series.to_frame()
    count_df = count_df.rename(columns={'survey_date': 'date_count'})
    count_df['survey_date'] = count_df.index
    count_df = count_df.reset_index(drop=True)
    print(count_df.info())
    print(count_df.head(50).to_string())

    sns.set()
    sns.relplot(x='survey_date', y='date_count', data=count_df)
    plt.show()


def chart_deficiencies_by_facility(deficiencies_df, providers_df, provider):
    print()
    provider_name = providers_df.loc[providers_df['federal_provider_number'] == provider, 'legal_business_name'].item()
    print(f'Filtering data for {provider_name}')

    user_deficiencies_df = deficiencies_df.loc[deficiencies_df.federal_provider_number == provider]

    user_deficiencies_df = pd.crosstab(user_deficiencies_df.survey_date, user_deficiencies_df.scope_severity_code)
    user_deficiencies_df['survey_date'] = user_deficiencies_df.index
    user_deficiencies_df = user_deficiencies_df.reset_index(drop=True)

    # print(user_deficiencies_df.info())
    # print(user_deficiencies_df.sort_values('survey_date').to_string())

    column_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'survey_date']

    template_df = pd.DataFrame(columns=column_names)

    for name in column_names:
        if name in list(user_deficiencies_df.columns):
            template_df[name] = user_deficiencies_df['{}'.format(name)]

    template_df = template_df.fillna(0)

    # print(template_df.to_string())

    user_annual_deficiencies_df = template_df.resample('Y', on='survey_date').sum()

    user_annual_deficiencies_df = user_annual_deficiencies_df.transpose()
    user_annual_deficiencies_df['scope_severity_code'] = user_annual_deficiencies_df.index
    user_annual_deficiencies_df = user_annual_deficiencies_df.reset_index(drop=True)

    temp_years_df = user_annual_deficiencies_df.drop(columns=['scope_severity_code'])
    temp_years_df = temp_years_df.rename(columns=lambda x: x.year)

    temp_codes_df = user_annual_deficiencies_df.loc[:, ['scope_severity_code']]

    user_annual_deficiencies_df = temp_years_df.join(temp_codes_df)

    # print(user_annual_deficiencies_df.info())
    # print(user_annual_deficiencies_df.to_string())

    sns.set(style='darkgrid')

    cmap = sns.blend_palette(["lightsalmon", "darkred"], 12)
    sns.set_palette(cmap, n_colors=12)

    ax = user_annual_deficiencies_df.set_index('scope_severity_code').T.plot(kind='bar',
                                                                             stacked=True,
                                                                             title=f'Deficiencies for {provider_name}',
                                                                             legend='reverse',
                                                                             color=cmap)

    ax.set_xlabel("year")
    ax.set_ylabel("number of deficiencies")

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1],
              labels[::-1],
              title='Severity',
              loc='center left',
              fontsize='x-small',
              bbox_to_anchor=(1.0, 0.5))

    plt.show()


def get_providers_from_owner(df):
    print()
    owner = input('Owner or organization of interest: ').upper()

    roles = input('Roles of interest:'
                  '\n[ 1 ] Officer'
                  '\n[ 2 ] Director'
                  '\n[ 3 ] Managing Employee'
                  '\n[ 4 ] Operational/Managerial Control'
                  '\n[ 5 ] 5% or greater direct ownership interest'
                  '\n[ 6 ] 5% or greater indirect ownership interest'
                  '\n[ 7 ] Partnership interest'
                  '\n[ 8 ] ALL ROLES'
                  '\n\nEnter roles by number: ')

    roles = roles.split(', ')
    translated_roles = []
    for role in roles:
        if int(role) == 1:
            translated_roles.append('OFFICER')
        if int(role) == 2:
            translated_roles.append('DIRECTOR')
        if int(role) == 3:
            translated_roles.append('MANAGING EMPLOYEE')
        if int(role) == 4:
            translated_roles.append('OPERATIONAL/MANAGERIAL CONTROL')
        if int(role) == 5:
            translated_roles.append('5% OR GREATER DIRECT OWNERSHIP INTEREST')
        if int(role) == 6:
            translated_roles.append('5% OR GREATER INDIRECT OWNERSHIP INTEREST')
        if int(role) == 7:
            translated_roles.append('PARTNERSHIP INTEREST')
        if int(role) == 8:
            break

    if translated_roles:
        print(f'Filtering data for {owner} by {translated_roles}...')
        owner_df = df.loc[df['owner_name'] == owner]
        owner_df = owner_df[owner_df.role.isin(translated_roles)]
    else:
        print(f'Filtering data for {owner} by all roles...')
        owner_df = df.loc[df['owner_name'] == owner]

    owner_df['tuples'] = list(zip(owner_df.federal_provider_number, owner_df.association_date))

    # print(owner_df.info())
    # print(owner_df.to_string())

    provider_list = owner_df.tuples.tolist()
    return provider_list, owner


def chart_deficiencies_by_owner(deficiencies_df, provider_list, owner):
    owner_deficiencies_df = pd.DataFrame

    for provider_tuple in provider_list:
        if provider_tuple[1] == 'NO DATE PROVIDED':
            provider_deficiencies_df = deficiencies_df.loc[deficiencies_df.federal_provider_number == provider_tuple[0]]
        else:
            provider_deficiencies_df = deficiencies_df.loc[deficiencies_df.federal_provider_number == provider_tuple[0]]
            temp_date = provider_tuple[1][6:]
            date = datetime.strptime(temp_date, '%m/%d/%Y')
            provider_deficiencies_df = provider_deficiencies_df[provider_deficiencies_df.survey_date >= date]
            # print(date)
            # print(provider_deficiencies_df.to_string())

        provider_deficiencies_df = pd.crosstab(provider_deficiencies_df.survey_date,
                                               provider_deficiencies_df.scope_severity_code)

        if provider_tuple == provider_list[0]:
            owner_deficiencies_df = provider_deficiencies_df
        else:
            owner_deficiencies_df = pd.concat([owner_deficiencies_df, provider_deficiencies_df], axis=1)
            owner_deficiencies_df = owner_deficiencies_df.groupby(owner_deficiencies_df.columns, axis=1).sum()

    owner_deficiencies_df['survey_date'] = owner_deficiencies_df.index
    owner_deficiencies_df = owner_deficiencies_df.reset_index(drop=True)

    column_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'survey_date']

    template_df = pd.DataFrame(columns=column_names)

    for name in column_names:
        if name in list(owner_deficiencies_df.columns):
            template_df[name] = owner_deficiencies_df['{}'.format(name)]

    template_df = template_df.fillna(0)

    owner_annual_deficiencies_df = template_df.resample('Y', on='survey_date').sum()

    owner_annual_deficiencies_df = owner_annual_deficiencies_df.transpose()
    owner_annual_deficiencies_df['scope_severity_code'] = owner_annual_deficiencies_df.index
    owner_annual_deficiencies_df = owner_annual_deficiencies_df.reset_index(drop=True)

    temp_years_df = owner_annual_deficiencies_df.drop(columns=['scope_severity_code'])
    temp_years_df = temp_years_df.rename(columns=lambda x: x.year)

    temp_codes_df = owner_annual_deficiencies_df.loc[:, ['scope_severity_code']]

    owner_annual_deficiencies_df = temp_years_df.join(temp_codes_df)

    sns.set(style='darkgrid')

    cmap = sns.blend_palette(["lightsalmon", "darkred"], 12)
    sns.set_palette(cmap, n_colors=12)

    ax = owner_annual_deficiencies_df.set_index('scope_severity_code').T.plot(kind='bar',
                                                                              stacked=True,
                                                                              title=f'Deficiencies for {owner}',
                                                                              legend='reverse',
                                                                              color=cmap)

    ax.set_xlabel("year")
    ax.set_ylabel("number of deficiencies")

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1],
              labels[::-1],
              title='Severity',
              loc='center left',
              fontsize='x-small',
              bbox_to_anchor=(1.0, 0.5))

    plt.show()


def get_ownership_info(owners_df, providers_df):
    # print(owners_df.info())
    # print(owners_df.head().to_string())
    #
    # print(providers_df.info())
    # print(providers_df.head().to_string())

    provider = input('Provider of interest: ').upper()
    provider_number = providers_df.loc[providers_df.legal_business_name == provider, 'federal_provider_number'].iloc[0]

    provider_owners_df = owners_df.loc[owners_df.federal_provider_number == provider_number]
    provider_owners_df = provider_owners_df.reset_index()
    provider_owners_df = provider_owners_df.rename(columns={'index': 'id'})
    print(provider_owners_df.to_string())

    print()
    selection = input('Select owners by number (or type "all" to select all): ')
    selection = selection.split(', ')
    print('Filtering data...')

    if selection != ['all']:
        provider_owners_df = provider_owners_df[provider_owners_df.index.isin(selection)]

    # print(provider_owners_df.to_string())

    name_list = provider_owners_df.owner_name.tolist()
    owners_df = owners_df.loc[owners_df.owner_name.isin(name_list)]
    # print(owners_df.head(50).to_string())

    owners_counts_df = pd.crosstab(owners_df.federal_provider_number, owners_df.owner_name)
    owners_counts_df = owners_counts_df.replace(0, np.nan).dropna(axis=0, how='any')
    # print(owners_counts_df.head(50).to_string())

    provider_list = owners_counts_df.index.tolist()
    print('Your exact selection is also involved here: ')

    their_providers = providers_df.loc[providers_df.federal_provider_number.isin(provider_list)]
    print(their_providers.to_string())


def get_ownership_groups(owners_df):
    direct_owners_df = owners_df.loc[owners_df.role == 'PARTNERSHIP INTEREST']
    counts = direct_owners_df.owner_name.value_counts()
    counts.to_csv('partnership_interest_counts.csv')


if __name__ == '__main__':
    main()
