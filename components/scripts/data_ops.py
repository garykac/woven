# Valid Minor Actions
valid_ops = [
    'tapestry',       # Draw tapestry card
    'eye',            # Create eye
    'emove2',         # Move eye
    'mmove',          # Move mage
    'thread',         # Recover thread
    'tmove',          # Move thread
    'action',         # Take another action

    'tapestry-eye',   # Draw tapestry card OR Create eye
    'tapestry-emove2', # Draw tapestry card OR Move eye
    'tapestry-mmove', # Draw tapestry card OR Move mage
    'tapestry-thread',# Draw tapestry card OR Recover thread
    #'tapestry-tmove', # Draw tapestry card OR Move thread
    #'tapestry+action', # Draw tapestry card AND take another action

    'eye-emove2',      # Create eye OR Move eye
    'eye-mmove',      # Create eye OR Move mage
    'eye-thread',     # Create eye OR Recover thread
    'eye-tmove',      # Create eye OR Move thread
    'eye+action',     # Create eye AND take another action

    'emove2-mmove',    # Move eye OR Move mage
    'emove2-thread',   # Move eye OR Recover thread
    'emove2-tmove',    # Move eye OR Move thread
    #'emove2+action',   # Move eye AND take another action

    'mmove-thread',   # Move mage OR Recover thread
    #'mmove-tmove',    # Move mage OR Move thread
    'mmove+action',   # Move mage AND take another action

    #'thread+action',  # Recover thread AND take another action
    #'thread-tmove',   # Recover thread OR Move thread - This pairing never makes sense since Recover is always better.

    'tmove+action',   # Move thread AND take another action

    #'action+action',  # Take another 2 actions
]
