from behave import given, when, then

from IPython import embed

@given('an anonymous user')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/admin/login/')

    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

@when('I submit a valid login page')
def step_impl(context):
    pass

@then('I am redirected to the login success page')
def step_impl(context):
    pass

@when('I submit an invalid login page')
def step_impl(context):
    pass

@then('I am redirected to the login fail page')
def step_impl(context):
    assert 1 == 1
