========================
Cut Copy Paste Delete 
========================

This software Cut Copy, Paste  Rename and Delete support for content
components in Cromlech.  In particular, it defines the following
interfaces for this kind of functionality:

* ``IObjectCutter``,

* ``IObjectCopier``,

* ``IObjectPaster``,
  
* ``IObjectRenamer``,

* ''IObjectDeleter''


This package  originally based on zope.copypastemove.  But then I tossed
out all of the old stuff.  It was just way way too complicated.

The new system is that here is a hidden folder at the root.  Cut and copied
objects go there.  Pasted objects are taken from there.  For multiple users,
it can have sub folders by user id. 

The big advantage is that this is way way simpler, easier to understand and
debug. This also leans heavily on whether an object provides
IMoveale, Icopyale, Irenameale and IDeleteable. 

INameChooser was thrown out.  It used to do lots of error checks.
Just use python-slugify to turn it into a valid name for uRLS.

Tossed out the whole annotations and principal clipboard.

If there are multiple copies
they get named oringinal-name_Copy1 oringinal-name_Copy2, etc.

Tosts out the whole zope.container.constraints thing.  Never used it.

Deleted tons of text from the source code.
They should not be in the source code.  It is just noise.
Referenced them in zope.copypastemove.

The code is now way simpler, easier to understand and debug.
It is easily readable. 
