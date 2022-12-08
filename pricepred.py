import typer
import logging
from helpers.helpers import AppSettings  # , GlobalVariables,
from helpers.validators import suburb_validator, address_validator, rooms_validator, type_validator, method_validator, \
    sellerg_validator, date_validator, postcode_validator, regionname_validator, \
    propertycount_validator, distance_validator, councilarea_validator
from modules.data_preprocess import DataPreprocess
from modules.ml_model import MlModelCreation
from typing import Optional
import os

__version__ = "0.0.1"

if AppSettings.use_logs == 1:
    logging.basicConfig(filename=os.path.join('logs', 'application.log'), level=AppSettings.logging_level,
                        format='%(asctime)s.%(msecs)03d : %(levelname)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

if AppSettings.return_console_messages == 0:
    def _disable_console_messages(*args, **kwargs):
        pass


    typer.echo = _disable_console_messages


def version_callback(value: bool):
    if value:
        typer.echo(f"Price Pred, version: {__version__}")
        raise typer.Exit()


def main(suburb: str = typer.Argument(..., help="Suburb", callback=suburb_validator),
         address: str = typer.Argument('2', help="Address", callback=address_validator),
         rooms: str = typer.Argument('3', help="Rooms", callback=rooms_validator),
         type: str = typer.Argument('4', help="Type", callback=type_validator),
         method: str = typer.Argument('5', help="Method", callback=method_validator),
         sellerg: str = typer.Argument('6', help="Seller G", callback=sellerg_validator),
         date: str = typer.Argument('7', help="Date", callback=date_validator),
         postcode: str = typer.Argument('8', help="Postcode", callback=postcode_validator),
         regionname: str = typer.Argument('9', help="Region name", callback=regionname_validator),
         propertycount: str = typer.Argument('10', help="Property count", callback=propertycount_validator),
         distance: str = typer.Argument('11', help="Distance", callback=distance_validator),
         councilarea: str = typer.Argument('12', help="Council Area", callback=councilarea_validator)
         ):
    """
    Entry point for application! Provide required information in order to proceed.
    Made by: Marek Hołowiecki (https://github.com/mholowiecki)
    """
    logging.debug(f"[Starting application with arguments:")
    data_preprocessed = DataPreprocess()
    ml_model = MlModelCreation(data_preprocessed.split_dict_of_data_frames)

    print(suburb)
    print(address)
    print(rooms)
    print(type)
    print(method)
    print(sellerg)
    print(date)
    print(postcode)
    print(regionname)
    print(propertycount)
    print(distance)
    print(councilarea)


# def run_statistics(country_code: str, output_currency: str, percentile_2: int, percentile_3: int,
#                   lower_threshold: float, higher_threshold: float, save_raw_data: bool, start_date: str, end_date: str, use_chosen: bool) -> str:
#    if percentile_3 <= percentile_2:
#        error = f"[{GlobalVariables.country_name.upper()}] " \
#                f"Third percentile is greater or equal than second! Change input data to continue."
#        typer.echo(error)
#        logging.critical(error)
#        raise typer.Abort()
#
#    logging.info(f"[{GlobalVariables.country_name.upper()}] Running statistics")
#    typer.echo(f"[{GlobalVariables.country_name.upper()}] Running statistics (it might take few minutes...)")
#    statistics_creator = StatisticsCreator(country_code2=country_code,
#                                           output_currency=output_currency,
#                                           start_date=start_date,
#                                           end_date=end_date)
#    StatisticsCreator.final_df = statistics_creator.get_final_df()
#
#    draft_df = statistics_creator.mean_column_creator(StatisticsCreator.final_df, percentile_2, percentile_3)
#
#    StatisticsCreator.final_df['2nd_percentile'] = draft_df['2nd_percentile']
#    StatisticsCreator.final_df['3nd_percentile'] = draft_df['3nd_percentile']
#    StatisticsCreator.final_df['avg_2&3_percentile'] = draft_df['avg_2&3_percentile']
#
#    StatisticsCreator.final_df = statistics_creator.calculate_percent(StatisticsCreator.final_df)
#    StatisticsCreator.final_df = statistics_creator.aberration_remover(StatisticsCreator.final_df,
#                                                                       lower_threshold, higher_threshold)
#
#    if use_chosen:
#        StatisticsCreator.final_df = statistics_creator.use_only_chosen_columns(StatisticsCreator.final_df,
#                                                                                start_date, end_date)
#        StatisticsCreator.final_df = statistics_creator.calculate_percent_chosen(StatisticsCreator.final_df)
#        StatisticsCreator.final_df = statistics_creator.remove_unused_columns(StatisticsCreator.final_df)
#
#    else:
#        StatisticsCreator.final_df = statistics_creator.calculate_percent(StatisticsCreator.final_df)
#        # PivotCreator.final_df = statistics_creator.add_sum_percentage_column(PivotCreator.final_df)
#        StatisticsCreator.final_df = statistics_creator.remove_unused_columns(StatisticsCreator.final_df)
#
#    statistics_filepath = statistics_creator.save_dataframe_to_excel(StatisticsCreator.final_df)
#    if save_raw_data:
#        statistics_creator.save_dataframe_to_csv(StatisticsCreator.final_df)
#
#    return statistics_filepath
#
#
# def run_excel_pivoting(statistics_filepath: str, output_currency: str):
#    logging.info(f"[{GlobalVariables.country_name.upper()}] Running Excel pivoting")
#    typer.echo(f"[{GlobalVariables.country_name.upper()}] Running Excel pivoting")
#    excel_client = ExcelClient(statistics_filepath, output_currency)
#    excel_client.pivot_excel_file()
#
#    return True
#
#
# def main(
#        # filename: str = typer.Argument(...,
#        #                                 help="Filename (ZIP extract) to be processed", callback=zipfile_validator),
#        country_code: str = typer.Argument(...,
#                                           help="Country code (ISO alpha-2)", callback=country_code_validator_2),
#        output_currency: str = typer.Option("euro", help="Choose output currency. Enter 'euro' or 'local'.",
#                                            callback=output_currency_validator),
#        second_percentile: int = typer.Option(40, help="Choose value of 2nd percentile. Integer value 0 - 100. "
#                                                       "See documentation for more information.",
#                                              callback=percentiles_validator),
#        third_percentile: int = typer.Option(60, help="Choose value of 3rd percentile. Integer value 0 - 100. "
#                                                      "Third percentile must be greater than second percentile! "
#                                                      "See documentation for more information.",
#                                             callback=percentiles_validator),
#        lower_threshold: float = typer.Option(0.2, help="Value of lower threshold. Range: 0.0 - 1.0. "
#                                                        "See documentation for more information.",
#                                              callback=threshold_validator),
#        higher_threshold: float = typer.Option(0.2, help="Value of lower threshold. Range: 0.0 - 1.0. "
#                                                         "See documentation for more information.",
#                                               callback=threshold_validator),
#        start_date: str = typer.Option(None, help="Start date for the statistics. For example: 2018-12-01 ("
#                                                  "yyyy-mm-dd). See documentation for more information."),
#        end_date: str = typer.Option(None, help="Start date for the statistics. For example: 2018-12-01 ("
#                                                "yyyy-mm-dd). See documentation for more information."),
#        use_chosen: bool = typer.Option(False, help="Decide whether to use only chosen columns ."),
#        save_raw_data: bool = typer.Option(True, help="Decide whether to save raw data to CSV file."),
#        version: Optional[bool] = typer.Option(None, "--version", callback=version_callback)
#
# ):
#    """
#    Entry point for application! Provide required information in order to proceed.
#    Made by: Marek Hołowiecki (https://github.com/mholowiecki)
#    """
#    logging.debug(
#        f"[{GlobalVariables.country_name.upper()}] Starting application with arguments: {country_code}")
#    GlobalVariables.country_code_2 = country_code
#    typer.echo(f"[{GlobalVariables.country_name.upper()}] App version: " + str(__version__))
#    typer.echo(f"[{GlobalVariables.country_name.upper()}] Country code: " + country_code)
#    typer.echo(f"[{GlobalVariables.country_name.upper()}] Output currency: " + output_currency)
#    typer.echo(f"{second_percentile}, {third_percentile}, {lower_threshold}, {higher_threshold}")
#
#    typer.secho("\nDuring this process Excel application will appear on your screen. \n"
#                "Please do not interfere with it. "
#                "It will close itself after process is done. \n", fg=typer.colors.YELLOW)
#
#    GlobalVariables.exchange_rate, GlobalVariables.currency_code = get_exchange_rate(country_code)
#    GlobalVariables.exchange_rate_to_local, GlobalVariables.currency_code = get_local_exchange_rate(country_code)
#
#    GlobalVariables.start_date = date_validator(start_date, country_code)
#    GlobalVariables.end_date = date_validator(end_date, country_code)
#
#    if GlobalVariables.start_date is None:
#        GlobalVariables.start_date = min(GlobalVariables.extracts_list)
#
#    if GlobalVariables.end_date is None:
#        GlobalVariables.end_date = max(GlobalVariables.extracts_list)
#
#    logging.debug(GlobalVariables.start_date)
#    logging.debug(GlobalVariables.end_date)
#
#    statistics_results = run_statistics(country_code, output_currency,
#                                        percentile_2=second_percentile, percentile_3=third_percentile,
#                                        lower_threshold=lower_threshold, higher_threshold=higher_threshold,
#                                        save_raw_data=save_raw_data,
#                                        start_date=GlobalVariables.start_date,
#                                        end_date=GlobalVariables.end_date,
#                                        use_chosen=use_chosen)
#
#    excel_pivot = run_excel_pivoting(statistics_results, output_currency)
#
#    if excel_pivot:
#        typer.echo(f"[{GlobalVariables.country_name.upper()}] Done! See results in output folder.")
#        logging.info(f"[{GlobalVariables.country_name.upper()}] Done! See results in output folder.")


if __name__ == '__main__':
    app = typer.Typer(add_completion=False)
    typer.run(main)
