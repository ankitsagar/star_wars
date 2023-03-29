# Django
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch, Q


class BaseService:
    model = None

    def get_by_id(self, obj_id: int):
        try:
            obj = self.model.objects.get(id=obj_id)
        except ObjectDoesNotExist:
            obj = None
        return obj

    def get_all(self):
        return self.model.objects.all()

    def bulk_create(self, data):
        """
        Accepts list of dict as data which can have all the required fields
        to create object
        """
        objs = []
        fields = [field.name for field in self.model._meta.get_fields()]
        for d in data:
            for key in list(d.keys()):
                if key not in fields:
                    d.pop(key)
            objs.append(self.model(**d))
        self.model.objects.bulk_create(objs=objs)


class BaseServiceWithUserMedataModel(BaseService):
    user_level_metadata_model = None
    user_level_metadata_rel_name = None
    user_level_metadata_attr_name = None
    model_id_field_in_user_metatdata = None
    model_field_in_user_metadata = None
    model_name_field = None

    def get_with_user_metadata_entries(self, user, query=None):
        """
        Fetches all the model instances with user level relation object if
        there are entries.
        """
        filter_args = []
        if query:
            user_level_metadata_queryset = self.get_user_metadata_entries(
                user_id=user.id, query=query
            )
            # These are the found model instance ids which need to be included
            # in the result
            model_ids_to_include = [
                getattr(user_data, self.model_id_field_in_user_metatdata)
                for user_data in user_level_metadata_queryset
            ]

            # These ids will be exculded in search at model level since there
            # are user level metadata already available
            model_ids_exculde_search = self.get_user_metadata_entries(
                user_id=user.id
            ).values_list(self.model_id_field_in_user_metatdata, flat=True)

            # We need to apply a filter on the table when the name contains
            # the query then it must not be the part of user metadata table and
            # include the result ids from user metadata table
            filter_args.append(
                (
                    Q(**{self.model_name_field + "__icontains": query}) &
                    ~Q(id__in=model_ids_exculde_search)
                ) | Q(id__in=model_ids_to_include)
            )
        else:
            user_level_metadata_queryset = self.get_user_metadata_entries(
                user_id=user.id
            )

        objs = self.model.objects.prefetch_related(
            Prefetch(
                self.user_level_metadata_rel_name,
                to_attr=self.user_level_metadata_attr_name,
                queryset=user_level_metadata_queryset
            )
        ).filter(*filter_args)
        return objs

    def get_user_metadata_entries(self, user_id, query=None):
        """ Return all the entries related to the user """
        queryset = self.user_level_metadata_model.objects.filter(
            user_id=user_id)
        if query:
            queryset = queryset.filter(custom_name__icontains=query)
        return queryset

    def get_user_metdata_entry(self, user_id, model_id):
        try:
            user_metadata_entry = self.user_level_metadata_model.objects.get(
                **{
                    "user_id": user_id,
                    self.model_id_field_in_user_metatdata: model_id
                }
            )
        except ObjectDoesNotExist:
            user_metadata_entry = None
        return user_metadata_entry

    def create_or_update_user_metadata_entry(
            self, model_instance, user, is_favorite, custom_name=None):
        user_metadata_entry = self.get_user_metdata_entry(
            user.id, model_instance.id)
        if not user_metadata_entry:
            user_metadata_entry = self.user_level_metadata_model(
                 **{
                    "user": user,
                    self.model_field_in_user_metadata: model_instance}
                 )
        user_metadata_entry.is_favorite = is_favorite
        # If custom name is none then attach the orignal name
        user_metadata_entry.custom_name = custom_name or getattr(
            model_instance, self.model_name_field)
        user_metadata_entry.save()
        return user_metadata_entry
