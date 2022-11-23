# Valid Minor Actions
valid_ops = [
    'tapestry',       # Draw tapestry card
    'tapestry-eye',   # Draw tapestry card OR Create eye
    #'tapestry-emove', # Draw tapestry card OR Move eye
    'tapestry-mmove', # Draw tapestry card OR Move mage
    'tapestry-thread',# Draw tapestry card OR Recover thread
    #'tapestry-tmove', # Draw tapestry card OR Move thread
    'eye',            # Create eye
    #'eye-emove',      # Create eye OR Move eye
    'eye-mmove',      # Create eye OR Move mage
    'eye-thread',     # Create eye OR Recover thread
    #'eye-tmove',      # Create eye OR Move thread
    'eye+action',     # Create eye AND take another action
    #'emove',          # Move eye
    #'emove-mmove',    # Move eye OR Move mage
    #'emove-thread',   # Move eye OR Recover thread
    #'emove-tmove',    # Move eye OR Move thread
    'emove+action',   # Move eye AND take another action
    'mmove',          # Move mage
    'mmove-thread',   # Move mage OR Recover thread
    #'mmove-tmove',    # Move mage OR Move thread
    'mmove+action',   # Move mage AND take another action
    'thread',         # Recover thread
    'thread+action',  # Recover thread AND take another action
    #'thread-tmove',   # Recover thread OR Move thread
    'tmove',          # Move thread
    'tmove+action',   # Move thread AND take another action
    'action',         # Take another action
    'action+action',  # Take another 2 actions
]
