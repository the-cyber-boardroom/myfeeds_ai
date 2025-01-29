from osbot_utils.type_safe.Type_Safe     import Type_Safe


class Model_OSS__Base(Type_Safe):                                         # Base model with common fields
    title          : str
    content        : str
    description    : str
    type           : str
    url            : str
    permalink      : str
    when_day       : str
    when_month     : str
    when_year      : int
    when_time      : str
    status         : str