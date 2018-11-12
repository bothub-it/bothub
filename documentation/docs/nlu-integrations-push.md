---
id: tutorial_en
title: Unite the power of Bothub with Push
sidebar_label: Push
---

## Creating your account on Push

> Push it's a development interface created to build smart and connectible to various toll's features. Used to improve companies' Customer Service, lead capture, make researches e keep a close relationship with clients, [Push](https://push.ilhasoft.mobi)'s chatbots are available to connect on most channels: websites, WhatsApp, Facebook Messenger, SMS, Android, iOS, Telegram, Twitter, Line and Viber.

To have access to this resources start by creating your **Account** and **Organization**.

Just [click here](https://push.ilhasoft.mobi/org/signup) and follow the next steps:

1. Fill below fields and click **Continuar**.

![CreateAccount](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/a9dd37aa-f543-4302-beda-1a817226e415.jpeg "Fill these field and hit next")

2. **Organization** will be the "workspace" where you'll develop the actions. Name it and click **Continuar**.

> To identify system components, like Organization name, it's a good practice not to use special characters (eg. **@ # $ %**).

![CreateOrg](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/a821042e-4f05-4db2-b9a9-fe3367f1e081.jpeg "Name your Organization and hit next")

3. You'll be redirected to [welcome](https://push.ilhasoft.mobi/welcome/?start) page with a short description of the main available tools. When needed to connect to your Organization, access your home: [https://push.ilhasoft.mobi](https://push.ilhasoft.mobi).

## Adding a channel to your Organization

On the website's top right corner, you can access the development tools of your Organization. By clicking its name, you shall access properties.
![Options](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/13d4b5f8-6e70-4a92-845b-40e0e9c0ff0a.jpeg "Development options")

There are many kinds and ways of available channels for you to integrate. 
Let's add Telegram and see how will the chat work? It's very easy!

1. Click at your Organization's name and then, at the engine icon right below the development options and choose [Add channel](https://push.ilhasoft.mobi/channels/channel/claim).

![AddChannel](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/8f53eeec-9bc7-4811-b51a-2a6ba6505378.jpeg "hit Add channel")

2. Scroll down until you see **Telegram** option and click on it.

![TelegramChannel](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/29251326-e617-42dc-9573-87c2390e07b8.jpeg "Hit Telegram")

3. Follow the next three steps and [Bot Father](https://telegram.me/botfather) shall provide a **Token ID**.
Next, copy that Token, paste it on the field **Token de autenticação** and click on **Enviar**.

![TelegramToken](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/7a9fcb70-0219-4717-8465-12e38361a664.jpeg "Paste your Token and hit Send")

4. That's it. Your Telegram chat is now connected to the Organization.

![TelegramStatus](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/7a9fcb70-0219-4717-8465-12e38361a664.jpeg "Channel status window")

## Building the chat

Now we need to create the messages exchange actions. These actions, the ones that shall have direct contact with the user, are developed in **Flows** option.
When you open that option, you'll see three sample flows created by the system to show you basic tool development features.

Click on **Sample Flow - Simple Poll** to open this flow.
![Flows](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/abdb90a7-fba3-4c48-9cb2-4c108a2f104b.jpeg "Hit this line to open the flow")

**Ready to see some magic?!** There are many development options in order to reach a fluid and continuous chat between actions, and here is where you'll able to build it.

This flow has just two kinds of actions: **Send Message** and **Wait for response**.
![FlowTemplate](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/14e4f746-f23f-4ec3-93c9-6f34084c5b3b.jpeg "Sample actions that a flow can have")

On our [knowledge base](https://push.al/documentacao-chatbot-push), it's available an [action list](https://push.al/knowledge_base/comandos-de-acao) with each description.

To allow the user to reach this flow and interact with the action build, it's necessary a [**trigger**](https://push.al/knowledge_base/criando-um-disparador-de-palavra-chave).
At this example, we'll create a simple kind of trigger, called **Keyword trigger**. To do it, access **trigger** session and choose the first option *Create a keyword trigger*.

![KeywordTrigger](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/365ab3d0-1e35-44db-acef-80cf83be8cbd.jpeg "Create the flow trigger")

Type the keyword, select the flow to be launched and click on **Criar disparador**.

![TutorialTrigger](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/670cb687-1bc7-4194-807f-1a8cdd3e9a30.jpeg "Hit create to make the flow trigger")

When the user sends the keyword to your Telegram chat, connected to Push system, the chosen flow will launch.

> Messages there are not triggers shall be received by your Org on Push, however it will be stored in *Inbox*. To take actions accordingly to the first message sent it's necessary to create a strategy to start a flow through triggers.
> Messages sent when the user is already inside a flow will be saved in *Flows*, on **Messages** option.

## Improving your chat with NLP

To filter a message according to its content, we can use a simple check of words and categorize it. However, besides being less flexible, this kind of filter is limited to words directly associated.
For instance, to filter a positive reply, we can use words like *Yes, Sure, ok, nice...*
What if the user misspells the word? Or even use most common chat texting words, like: *Yep, Yup, Yeah, y...*
Well, this other words must also be manually added to the category filter!
Now imagine having to administrate many flows, orgs and distinguished projects... That's not productive, right? 

And if I said that we can ally this variety of category types within a simple message with an intent algorithm which is capable of translating an entire message on a single **intent**? Wouldn't that be great?
And this is just one of the advantages of using NLP (Natural Processing Language) allied to your flows.

With [Bothub](https://bothub.it), you'll be able to add natural language processing on multiple and most distinguished strategies. Using a collaborative model, it's possible to contribute to current existent training or create yours and invite more people to help building more content by adding new examples to your intent repository.

Shall we create your account? Access [https://bothub.it](https://bothub.it) and click **sign in** on top right corner.

![BotHubHome](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/dc0c4c98-81c2-4efa-9511-18fc64eedbaa.jpeg "Hit sign in")

Choose **Create account**, fill the field with your data and click **Register**.

![BotHubRegister](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/a5bae530-96b7-4cd6-af07-277748243d9a.jpeg "Hit Register after filling the fields")

To login just change the tab to **Login** and type your credentials.

The next step is creating your repository and start adding examples on it. On the top right of the window, click **start your bot**. Fill the fields and click **Create bot**.

![BotHubTrainning](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/291e319c-702d-4eda-8455-30da99202ada.jpeg "Fill the fields and hit Create bot")

Now start adding content to your interpretation mechanism by providing phrases examples. To do it, choose **Examples**, you'll see a field and an option to categorize it.
On this current process, we'll add examples related to detecting *positives* or *negatives* intents.

All you have to do is type the phrase (or word) and relate that to its intent.

![BotHubExample](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/4cd09121-064c-4b20-b986-e0c6205ab4d0.jpeg "Type the example and point to its category")

I made a video adding a few examples, take a look.
[![](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/ff103911-9952-48b7-b1a4-1ac7d3c3838f.jpeg)](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/741df39e-e83e-456a-9dd0-c879a82441c5.mp4)

Once adding examples is done, you must commit the updates made. To do it, click **Train**.

![BotHubSave](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/3c0324f7-aff2-4e49-8895-7e269bf08ef1.jpeg "Save the training updates")

## Intengrating the Bothub trainning to your Organization

Now that we have an NLP repository available it's needed to add that mechanism to flows so messages can be analyzed by.

Still on Bothub, acces **Analyze Text** tab and copy the *Authorization* code from your repository.

![BotHubToken](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/1696a369-35dd-4bd7-894e-4ab8f16d5e33.jpeg "Copy the Authorization token")

Now back to Push, click on the Organization name to access its properties, scroll down until you see **Connect your Bothub repository** option and click on it.
Paste the token you just got from Bothub and click **Add token**.

![BotHubPush](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/45e28511-b901-42a5-8001-d9106cb00a5c.jpeg "Add and save your repository's token")

And that's it! Now let's make the added repository work with the example flow we used on the beginning of this post.

Go to **Flows** area by clicking its option on the top of your window and again choose *Sample Flow - Simple Poll*.
On the flow's action window, click on the *Wait for Filter Working* to edit it and modify the first rule's column from *has any of these words* the last option *has an intent*.

You'll see there're other kinds of filters to each response category.
![PushWFRkeyword](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/bee75862-4077-4123-afb6-d91ddfb298d7.jpeg "Modify the filter type")

It should look like this after modifying both grades.
![PushWFRintent](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/08d1c1bd-c9ee-4d46-9e45-680ecbec35c6.jpeg "Modify the filter type")

## Testing your chatbot

With your Telegram chat connected and finishing the flow, now you can talk to the chatbot!
Though the Telegram chat, send the keyword trigger that you've set, test it and tell us your thoughts about it! :)

Cya!

![Robotinho](https://udo-rapidpro-static-app.s3.amazonaws.com/attachments/191/6077/steps/f545e0a8-5c0b-4702-b2fd-5a08e4f2a1e1.png "Robotinho")



Collapse 
