# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-


# from cmk.gui.i18n import _

# from cmk.gui.valuespec import (
#     Dictionary,
#     Tuple,
#     Percentage,
# )
# from cmk.gui.plugins.wato import (
#     CheckParameterRulespecWithoutItem,
#     rulespec_registry,
#     RulespecGroupCheckParametersOperatingSystem,
# )

# def _valuespec():
#     return Dictionary(
#         elements = [
#             ("prefixes_sent", Tuple(
#                 title=_("Prefixes Sent"),
                
#             )),
#             ()
#         ]
#     )
#     pass

# rulespec_registry.registyer(
#     check_group_name = '',
#     group = RulespecGroup,
#     match_type = '',
#     parameter_valuespec = _valuespec, 
#     title=_(),
# )