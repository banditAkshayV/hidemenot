from msteamsapi import TeamsWebhook, AdaptiveCard, Container, FactSet, ContainerStyle, TextWeight, TextSize

webhook = TeamsWebhook('https://defaulte700286ed8144d0a98f7bb2984d70a.25.environment.api.powerplatform.com/powerautomate/automations/direct/workflows/0b149d0df963470abf3abd0d5fe343c5/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=SNppijel3YwKP0LiedfPC6nuFyLmoUG4aFCS3aAv1MQ')

card = AdaptiveCard(title='card title', title_style=ContainerStyle.DEFAULT)
card.add_background(url="https://github.com/ALERTua/msteamsapi/raw/main/tests/background.png")

container = Container(style=ContainerStyle.DEFAULT)

card.mention('EMAIL', 'NAME', add_text_block=True)
mention_tag = card.mention('EMAIL', 'mention text')

container.add_image("image url", "image alt text")
container.add_text_block(
    'multiline\n\ntext\n\nmention 1: %s' % mention_tag,
    size=TextSize.DEFAULT, weight=TextWeight.DEFAULT, color="default", wrap=True
)

factset = FactSet(('fact 1', 'fact 1 value'))
factset.add_facts(('fact 2', 'fact 2 value'), ('fact 3', 'fact 3 value'))
container.add_fact_set(factset)

card.add_container(container)

for i, url in enumerate(['https://google.com/', 'https://goo.gle']):
    card.add_url_button('url %s' % i, url)

webhook.add_cards(card)
webhook.send()