Kii flavored markdown
=====================

Objectives
**********

Kii flavored markdown aims to provide a clean, short syntax for referencing other kii objects such as streams, items, tags and users inside markdown content, without breaking markdown compatibility.

Users
*****

This is the easiest part, and we can follow the common ``@username`` pattern used at Github and Stackoverflow, which renders to::

    <a href="/link/to/user/profile">@username</a>

Stream, items and tags
**********************

The widely used hashtag syntax ``#ID`` seems the way to go. However, the traditionnal hash-mark/ID couple won't be enough because we need to reference different content types, and we cannot deduce the targeted object simply with an ID.

Also, we need different outputs depending on the content type. For exemple, keeping the tag slug preceded with the hash mark is ok for tags, but not so great if we're referencing a stream or an item: for these elements, we'll need a pretty output, with the title replacing the ID, and the hashmark hidden. Users may even need to provide a custom link anchor, in case they want to include the link inside their sentence.

So, the syntax should have following behaviour:

- For tags: hash mark followed by tag slug
- For stream and items: hash mark followed by the content type and the targeted object ID
- For any content type: the possibility for the user to provide a custom link anchor. If no anchor is provided, the default object representation would be used, probably the object title.

So we end up with something like this:

For tags::

    #tagslug(Optionnal anchor)

For other objects::

    #contenttype/ID(Optional anchor)

.. note:: 

    ``ID`` may refer to an integer identifier but also to a slug (e.g. for streams)