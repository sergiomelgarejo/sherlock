import pandas as pd
import numpy as np


class Sherlock:
    """Una clase usada para representar un limpiador de datos.

    ...

    Attributes
    ----------
    datasource : str,
        origen de los datos:
              
            - path del archivo, cuando se trata de un archivo Excel, csv, etc.
            - query, cuando se trata de una consulta SQL.

    Examples
    --------
    >>> objeto = Sherlock('file.xlsx')
    >>> objeto = Sherlock('select * from empleados;')
    """

    def __init__(self, datasource):
        """Constructor de la clase.

        Args:
            datasource (str): Fuente de datos.
        """
        self.datasource = datasource


    def generar(self, sourcetype = 'sql') -> pd.DataFrame:  
        """ 
        Genera un DataFrame basado en el tipo de origen de datos.

        Parameters
        ----------
        sourcetype : {'sql', 'excel', 'csv'}, default 'sql'

            Determina el tipo de origen de datos usado para generar el DataFrame
            - ``sql`` : Define que la fuente de datos a utilizar es SQL.
            - ``excel`` : Define que la fuente de datos a utilizar es un archivo Excel.
            - ``csv`` : Define que la fuente de datos a utilizar es un archivo CSV.
    
        Returns
        -------
        DataFrame
        """ 

        if sourcetype == 'sql':
            df = pd.read_sql(self.datasource, db_connect())
        if sourcetype == 'excel':
            df = pd.read_excel(self.datasource)
        if sourcetype == 'csv':
            df = pd.read_csv(self.datasource)

        return df


    def buscar_duplicados(df, mantener='first') -> pd.DataFrame:
        """ 
        Genera un DataFrame con filas duplicadas.

        Parameters
        ----------
        df : DataFrame
            Datos estructurados de entrada en formato objeto DataFrame de Pandas.
        mantener : {'first', 'last', False}, default 'first'

            Determina cuales duplicados (si existe alguno) marcar.
            - ``first`` : Marca duplicados como ``True`` excepto la primera ocurrencia.
            - ``last`` : Marca duplicados como ``True`` excepto la última ocurrencia.
            - ``False`` : Marca todos los duplicados como ``True``.
    
        Returns
        -------
        DataFrame con todos los duplicados marcados como ``True``.

        Examples
        --------
        >>> columnas = ['ID', 'cedula']
        >>> objeto = Sherlock('select * from empleados;')
        >>> objeto.buscar_duplicados(df, mantener='first')
        """ 

        return df[df.duplicated(keep=keep)]


    def buscar_nulos(df, columns) -> pd.DataFrame:
        """ 
        Genera un DataFrame con los registros de las columnas con datos nulos.

        Parameters
        ----------
        df : DataFrame
            Datos estructurados de entrada en formato objeto DataFrame de Pandas.
        columns : list
            Lista de columnas a evaluar 
            por ej: IDs, columnas de cantidades, valores que no deben ser nulos o vacíos,
            datos obligatorios, etc.
    
        Returns
        -------
        DataFrame

        Examples
        --------
        >>> columnas = ['ID', 'cedula']
        >>> objeto = Sherlock('select * from empleados;')
        >>> objeto.buscar_nulos(df, columnas)
        """ 

        df_nulos = df[df[columns].isnull().any(axis=1)]


    def buscar_no_numericos(df, columns) -> pd.DataFrame:
        """ 
        Genera un DataFrame con todos los registros que contienen columnas 
        no numéricas de acuerdo a las columnas seleccionadas.

        Parameters
        ----------
        df : DataFrame
            Datos estructurados de entrada en formato objeto DataFrame de Pandas.
        columns : list
            Lista de columnas a evaluar 
            por ej: IDs, columnas de cantidades, valores que no deben ser nulos o vacíos,
            datos obligatorios, etc.

        Returns
        -------
        DataFrame

        Examples
        --------
        >>> columnas = ['ID', 'cedula']
        >>> df_no_num = objeto.buscar_no_numericos(df, columnas)
        """ 

        es_numerico = lambda col: df[col].str.contains('^[0-9]*$', regex=True)

        no_numericos = []
        if isinstance(columns, list):
            if len(columns) > 0:
                for column in columns:
                    df_aux = df[es_numerico(column) == False]
                    no_numericos.append(df_aux)

                appended_data = pd.concat(no_numericos)
            else:
                appended_data = pd.DataFrame()
        else:
            appended_data = df[es_numerico(columns) == False]
        
        return appended_data        


    def buscar_patron_regex(df, regex, columns) -> pd.DataFrame:
        """ 
        Genera un DataFrame con todos los registros de las columnas que cumplan
        con un patrón de expresión regular.

        Parameters
        ----------
        df : DataFrame
            Datos estructurados de entrada en formato objeto DataFrame de Pandas.
        regex : str
            Patrón de expresión regular.
        columns : list
            Lista de columnas a evaluar 
            por ej: IDs, columnas de cantidades, valores que no deben ser nulos o vacíos,
            datos obligatorios, etc.

        Returns
        -------
        DataFrame

        Examples
        --------
        >>> columnas = ['Email']
        >>> regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        >>> dfx = objeto.buscar_patron_regex(df, regex=regex, columns=columnas)
        """ 

        pattern = lambda col: df[col].str.contains(f'{regex}', regex=True)

        dfs = []
        if isinstance(columns, list):
            if len(columns) > 0:
                for column in columns:
                    df_aux = df[pattern(column) == True]
                    dfs.append(df_aux)

                appended_data = pd.concat(dfs)
            else:
                appended_data = pd.DataFrame()
        else:
            appended_data = df[pattern(columns) == True]
            
        appended_data 