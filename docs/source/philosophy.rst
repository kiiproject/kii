Philosophy
==========

Stream and items
****************

Kii is written with the notion of `stream` in mind. It's dead-simple: a stream belongs to a user, who can publish `items` in it. An item could be, for example, a blog entry, a picture, a link to a web page, or any type of content provided by third-party apps.

All items share a common behaviour:

- they support comments
- they get a unique permalink, which allow easy sharing over the web
- they support fine-grained permission. You can mark each of them as public, restricted to a set of users or groups or even entirely private if you want to
- they have a status, published or draft

Of course, this is just the common part. Derived content-types may offer additional behaviour, like syntax highlighting for code snippets.

Because of the common behaviour of items, kii offers various filtering options. While a stream index page will display every items, no matter what their type is, it's also possible to display only a specific content type. The same rule applies for feeds: one could subscribe to your entire stream, or only to your snippets.

Freedom
*******

The project is released under the MIT license, which means you are free to download, modify, and distribute it.


