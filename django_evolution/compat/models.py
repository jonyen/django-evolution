"""Compatibility functions for model-related operations.

This provides functions for working with models or importing moved fields.
These translate to the various versions of Django that are supported.
"""

try:
    # Django >= 1.7
    from django.apps.registry import apps
    from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                    GenericRelation)

    cache = None
    all_models = apps.all_models
    get_model = apps.get_model
    _get_models = None
except ImportError:
    # Django < 1.7
    from django.db.models.loading import (cache, get_model,
                                          get_models as _get_models)
    from django.contrib.contenttypes.generic import (GenericForeignKey,
                                                     GenericRelation)

    all_models = cache.app_models
    apps = None


def get_models(app_mod=None, include_auto_created=False):
    """Return the models belonging to an app.

    Args:
        app_mod (module, optional):
            The application module.

        include_auto_created (bool, optional):
            Whether to return auto-created models (such as many-to-many
            models) in the results.

    Returns:
        list:
        The list of modules belonging to the app.
    """
    if apps:
        # Django >= 1.7
        if app_mod is None:
            return apps.get_models(include_auto_created=include_auto_created)
        else:
            app_label = app_mod.__name__.split('.')[-2]

            try:
                app_config = apps.get_app_config(app_label)

                return list(app_config.get_models(
                    include_auto_created=include_auto_created))
            except LookupError:
                return []
    else:
        # Django < 1.7
        return _get_models(app_mod, include_auto_created=include_auto_created)


def set_model_name(model, name):
    """Set the name of a model.

    Args:
        model (django.db.models.Model):
            The model to set the new name on.

        name (str):
            The new model name.
    """
    if hasattr(model._meta, 'model_name'):
        # Django >= 1.7
        model._meta.model_name = name
    else:
        # Django < 1.7
        model._meta.module_name = name


def get_model_name(model):
    """Return the model's name.

    Args:
        model (django.db.models.Model):
            The model for which to return the name.

    Returns:
        str: The model's name.
    """
    if hasattr(model._meta, 'model_name'):
        # Django >= 1.7
        return model._meta.model_name
    else:
        # Django < 1.7
        return model._meta.module_name


def get_rel_target_field(field):
    """Return the target field for a field's relation.

    Args:
        field (django.db.models.Field):
            The relation field.

    Returns:
        django.db.models.Field:
        The field on the other end of the relation.
    """
    if hasattr(field, 'target_field'):
        # Django >= 1.7
        return field.target_field
    else:
        # Django < 1.7
        return field.related_field


__all__ = [
    'GenericForeignKey',
    'GenericRelation',
    'all_models',
    'get_model',
    'get_models',
    'get_model_name',
    'get_rel_target_field',
    'set_model_name',
]
