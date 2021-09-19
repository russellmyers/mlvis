import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mlvis

def has_header(df, data_delim=',', nrows=20):
#    df = pd.read_csv(uploaded_file)
    df.to_csv("tst_header.csv", index=False, header=None)
    df_1st_row = pd.read_csv("tst_header.csv", header=None, nrows=1)
    df_next_rows = pd.read_csv("tst_header.csv", header=None, skiprows=1, nrows=nrows)
    return tuple(df_1st_row.dtypes) != tuple(df_next_rows.dtypes), df_next_rows.dtypes

st.title("ML Visualisation")
st.caption(mlvis.__version__)

#data_delim = st.text_input("Data delimiter:",",")
uploaded_file = st.file_uploader("Upload csv file containing ml data (id field(s)/features/label)")
if uploaded_file is not None:
# has_header_row = st.checkbox('Data has header row?', value=True)
    try:
      df = pd.read_csv(uploaded_file, header=None)
    except Exception as e:
         st.write('Exception occurred reading file. Error is: {e}')
    has_header_row, next_rows_dtypes = has_header(df)
    st.write(f'Has header? {has_header_row}')
    if not has_header_row:
        def_names_list = [f'field_{n}' for n in range(1,len(df.columns)+1)]
        def_names = ','.join(def_names_list)
        df.columns = def_names_list
        #if column_names:
        #    st.sidebar.write(f'column names: {column_names}')
    else:
       df.columns = df.iloc[0]
       df = df.iloc[1:,:]
       def_names = ','.join(df.columns)
       for i, dt in enumerate(next_rows_dtypes):
           df[df.columns[i]] = df[df.columns[i]].astype(dt)
    column_names = st.sidebar.text_input('Column names:', def_names)
    try:

        st.subheader('Raw data:')
        st.write(df)


        all_columns = list(df.columns)
        id_columns = st.sidebar.text_input('Specify which columns, if any, are id fields (not features or labels) - delimited by comma', all_columns[0])
        feature_columns = st.sidebar.text_input('Specify which columns are  features - delimited by comma', ','.join(all_columns[1:-1]))
        if feature_columns:
            feature_column_names = feature_columns.split(',')
            show_descrip = st.checkbox("Show feature descriptions")
            if show_descrip:
                st.subheader('Feature descriptions')
                st.write(df[feature_column_names].describe())
            show_hists = st.checkbox('Show feature histograms')
            if show_hists:
                st.subheader('Feature histograms')
                feature_column_names = feature_columns.split(',')
                df_feat = df[feature_column_names]
                fig, ax = plt.subplots()
                df_feat.hist(ax=ax)
                plt.show()
                st.pyplot(fig)

            # # histogram
            # feature_column_names = feature_columns.split(',')
            # df_feat = df[feature_column_names]
            # fig, ax = plt.subplots()
            # df_feat.hist(ax=ax)
            # plt.show()
            # st.pyplot(fig)

        label_column = st.sidebar.text_input('Specify which column, if any, contains labels', all_columns[-1])
        if label_column:
            label_column_name = label_column
            show_label_desc = st.checkbox('Show label description')
            if show_label_desc:
                st.subheader('Label description')
                if df[label_column_name].dtype == 'object':
                    st.write(df[label_column_name].value_counts())
                else:
                    st.write(df[label_column_name].describe())
            # fig, ax = plt.subplots()
            #
            # df[label_column_name].hist(ax=ax)
            # plt.show()
            # st.pyplot(fig)


    except Exception as e:
        st.write(f'Error occured: {e}')



if __name__ == '__main__':
    print("Running from main")
    if False:
        df = pd.read_csv("tests/data/BCH-USD.csv", header=None)
        has_header_row, next_rows_dtypes = has_header(df)
        for i, dt in enumerate(next_rows_dtypes):
            df[df.columns[i]] = df[df.columns[i]].astype(dt)
        x = 1