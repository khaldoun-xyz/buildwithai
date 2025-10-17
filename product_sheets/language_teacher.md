# Product sheet: Language teacher

Let's practice our language skills!

Language students often have a theoretical understanding of
grammar and vocabulary but lack sufficient opportunities
to apply this knowledge in authentic, real-time conversations.

Provide an interface that lets a student select a language
and initiate a conversation via text message. The AI will then
engage in a chat conversation with the student in the student's
chosen language.

A student may choose to receive a score and evaluation. For this,
the student can ask for an evaluation, effectively ending the
conversation. He will then receive a report card that also contains
specific mistakes the user made.

You may also want to add additional learning modes (e.g. receive
bi-lingual message for easier understanding) or modalities (e.g.
have an audio conversation).

## Required features

- **Language Selection**: The user selects the target language
  at the start of a session.
- **Chat functionality**: The user can initiate and engage
  in a text-based conversation.
  The AI's responses must be exclusively
  in the selected target language.
- **Evaluation request**: A clear mechanism (e.g. a
  button or a specific text command like /evaluate)
  that allows the user to end the current conversation and
  request an evaluation report.
- **Evaluation report**: The system analyses the
  conversation transcript and generates a report.
  This report must include:
  - An overall performance score or summary.
  - A list of specific mistakes or awkward phrasings
    made by the user, along with suggested improvements.

## Optional Features

- **Bilingual learning mode**: An alternative mode the user can
  activate where each AI message is provided in both the target
  language and English for easier understanding.
- **Audio conversations**: Integrate Speech-to-Text and Text-to-Speech
  capabilities to allow the user to practice the conversation by
  speaking and listening, rather than typing.
- **Performance history**: Save past reports so the user can
  track the progress and review previous mistakes over time.
