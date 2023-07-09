import logging



def setup_logger(log_file):
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set the log level
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handlers
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)

    return logger

# Usage example
logger = setup_logger('penetration_logv2.txt')




def payload_logging(outcome, source, extension_id, extension_name, url_of_website, payload, time_of_injection, time_of_alert, payload_filename):

  if outcome == "SUCCESS":
    logger.info(f"outcome: {outcome}, source: {source}, extensionId: {extension_id}, extensionName: {extension_name}, Url: {url_of_website}, payload: {payload}, timeOfInjection: {time_of_injection}, timeOfAlert: {time_of_alert}, payload_fileName: {payload_filename}")
  else:
    logger.info(f"outcome: {outcome}, source: {source}, extensionId: {extension_id}, extensionName: {extension_name}, Url: {url_of_website}, payload: {payload}, timeOfInjection: {time_of_injection}, timeOfAlert: {time_of_alert}, payload_fileName: {payload_filename}")


payload_logging("SUCCESS", "window.name", 'cjjdmmmccadnnnfjabpoboknknpiioge', 'h1-replacer(v3)', 'file:///test.html', '<img src=x onerror=alert("123")>', '2023-07-09 16:30:20,956', '2023-07-09 16:30:21,55', 'shit_ass_payload_file.txt')
payload_logging("FAILURE", "window.name", 'cjjdmmmccadnnnfjabpoboknknpiioge', 'h1-replacer(v3)', 'file:///test.html', '<img src=x onerror=alert("123")>', '2023-07-09 16:30:20,956', '2023-07-09 16:30:21,55', 'shit_ass_payload_file.txt')
