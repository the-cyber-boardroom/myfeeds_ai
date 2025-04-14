from enum import Enum


class Schema__Persona__Types(Enum):
    EXEC__CEO               : str = 'exec-ceo'
    EXEC__CISO              : str = 'exec-ciso'
    EXEC__CTO               : str = 'exec-cto'
    INVESTOR__ANGEL         : str = 'investor-angel'
    INVESTOR__SERIES_A      : str = 'investor-series-a'
    PRIVATE__CISO           : str = 'private-ciso'
    PRIVATE__BOARD_MEMBER   : str = 'private-board-member'
    PUBLIC__CISO            : str = 'public-ciso'
    PUBLIC__BOARD_MEMBER    : str = 'public-board-member'
    STARTUP__CISO           : str = 'startup-ciso'
    STARTUP__BOARD_MEMBER   : str = 'startup-board-member'
    TEAM__APP_SEC           : str = 'team-app-sec'
    TEAM__EXTERNAL_COMMS    : str = 'team-external-comms'
    TEAM__INCIDENT_RESPONSE : str = 'team-incident-response'
    TEAM__GRC               : str = 'team-grc'
    TEST__PERSONA           : str = 'test-persona'




