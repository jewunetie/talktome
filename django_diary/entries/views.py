from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Entry
from .backend_interface import OpenAIInterface, PineconeInterface


class LockedView(LoginRequiredMixin):
    login_url = "admin:login"


class EntryListView(LockedView, ListView):
    model = Entry
    queryset = Entry.objects.all().order_by("-date_created")


class EntryDetailView(LockedView, DetailView):
    model = Entry

from datetime import datetime

def convert_date_to_integer(date_obj):
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, "%B %d, %Y")
    return int(date_obj.strftime("%Y%m%d"))

class EntryCreateView(LockedView, SuccessMessageMixin, CreateView):
    model = Entry
    fields = ["title", "content"]
    success_url = reverse_lazy("entry-list")
    success_message = "Your new entry was created!"

    def form_valid(self, form):
        # Call OpenAIInterface.get_positive to get the positive version of the content
        positive_content = OpenAIInterface().get_positive(form.instance.content)

        # Update the positive_version of the Entry instance
        form.instance.positive_version = positive_content

        def convert_date_string_to_formatted_string(date_obj):
            # change the date_obj to "%B %d, %Y"
            date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S.%f%z")

            return date_str
        
        similar_entry = PineconeInterface().query(form.instance.content, convert_date_string_to_formatted_string(form.instance.date_created))

        # get the (identifier, score) tuple from similar_entry, get the journal entries
        journal_entries = Entry.objects.filter(id__in=[int(entry) for entry in similar_entry])

        print(journal_entries)

        # Call the find_pattern function to get the pattern
        contents = [entry.content for entry in journal_entries]
        contents.append(form.instance.content)
        pattern = OpenAIInterface().find_pattern(contents)
        print(pattern)
        form.instance.find_pattern = pattern

        # add the entry to the pinecone index
        form.instance.id = convert_date_to_integer(form.instance.date_created)
        print(form.instance.id)
        PineconeInterface().indexing(form.instance.content, str(form.instance.id))

        # Call the superclass method to save the object and return the response
        return super().form_valid(form)


class EntryUpdateView(LockedView, SuccessMessageMixin, UpdateView):
    model = Entry
    fields = ["title", "content"]
    success_message = "Your entry was updated!"

    def get_success_url(self):
        return reverse_lazy("entry-detail", kwargs={"pk": self.object.pk})
    
    def form_valid(self, form):
        # Call OpenAIInterface.get_positive to get the positive version of the content
        print(form.instance.content)
        positive_content = OpenAIInterface().get_positive(form.instance.content)



        # Update the positive_version of the Entry instance
        form.instance.positive_version = positive_content

        # Call the similarity function to get the most similar entry
        similar_entry = PineconeInterface().query(form.instance.content)

        print(similar_entry)

        # Call the superclass method to save the object and return the response
        return super().form_valid(form)


class EntryDeleteView(LockedView, SuccessMessageMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy("entry-list")
    success_message = "Your entry was deleted!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
