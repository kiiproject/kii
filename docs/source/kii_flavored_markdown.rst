Kii flavored markdown
=====================

Goals
*****

Kii flavored markdown aims to provide a clean, short syntax for referencing other kii objects such as streams, items, tags and users inside markdown content, without breaking markdown compatibility.

Referencing objects
*******************

Users
-----

Kii follows the common ``@username`` pattern used at Github and Stackoverflow, which renders to::

    <a href="/link/to/user/profile">@username</a>

Referencing stream and items
----------------------------

We use the Twitter syntax for tags, and a slightly more complex one for other content types.

For tags::

    #tagslug(Optionnal anchor)

For other objects::

    #contenttype/ID(Optional anchor)

    #stream/mystreamslug(Optional anchor)
    #item/44(Optional anchor)


.. note:: 

    Support of tag referencing will be included in a future release

.. note:: 

    ``ID`` may refer to an integer identifier but also to a slug (e.g. for streams)
  
.. warning::

    The hash-syntax does not work if the the hash pattern is in the first position of a paragraph, because it would be intepreted as a title by the markdown parser. 

