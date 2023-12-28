import { Component, EventEmitter, Output } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { validUrlValidator } from './util';
import { SubmitRequest } from '../types';

@Component({
  selector: 'app-create-feed-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './create-feed-form.component.html',
  styleUrl: './create-feed-form.component.scss',
})
export class CreateFeedFormComponent {
  @Output() submitRequest = new EventEmitter<SubmitRequest>();

  feedForm = this.formBuilder.group({
    url: ['', validUrlValidator()],
    field: ['title'],
    condition: ['exact match'],
    matchResult: ['include'],
    query: ['', Validators.compose([Validators.required])],
  });

  constructor(private formBuilder: FormBuilder) {}

  handleSubmit() {
    this.submitRequest.emit(this.feedForm.value as any);
  }
}
