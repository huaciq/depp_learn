import resend

resend.api_key = "re_9wEga6Wq_B214cJ5jaH1HrQ4w6UzvyAri"

params: resend.Emails.SendParams = {
  "from": "Acme <onboarding@957369.xyz>",
  "to": ["dasf@957369.xyz"],
  "subject": "hello world",
  "html": "<p>it works!</p>"
}

email = resend.Emails.send(params)
print(email)