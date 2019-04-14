from chatterbot import ChatBot
from chatterbot.conversation import Statement
import responses

from hr.bot.logic import wolframalpha

validate_result_success = """<?xml version='1.0' encoding='UTF-8'?>
<validatequeryresult success='true'
    error='false'
    timing='0.292'
    parsetiming='0.274'
    version='2.6'>
</validatequeryresult>
"""


def test_can_process_no_app_id():
    wa = wolframalpha.WolframAlpha(ChatBot("test-bot"))
    assert not wa.can_process(Statement("hello"))


@responses.activate
def test_can_process_success():
    responses.add(
        responses.GET,
        "https://api.wolframalpha.com/v2/validatequery",
        body=validate_result_success,
        status=200,
    )
    wa = wolframalpha.WolframAlpha(ChatBot("test-bot"), wolfram_alpha_app_id="abcd")
    assert wa.can_process(Statement("hello"))


@responses.activate
def test_can_process_tags():
    """It should not process when the adapter is disabled in the request."""
    responses.add(
        responses.GET,
        "https://api.wolframalpha.com/v2/validatequery",
        body=validate_result_success,
        status=200,
    )
    wa = wolframalpha.WolframAlpha(ChatBot("test-bot"), wolfram_alpha_app_id="abcd")
    statement = Statement("hello")
    statement.add_tags("disable_wolfram")
    assert not wa.can_process(statement)