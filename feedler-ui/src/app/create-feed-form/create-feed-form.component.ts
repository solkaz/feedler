import { Component, EventEmitter, Output, output } from '@angular/core';
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
  submitRequest = output<SubmitRequest>();

  feedForm = this.formBuilder.group({
    url: ['', [Validators.required, validUrlValidator()]],
    field: ['title', Validators.required],
    condition: ['exact match', Validators.required],
    matchResult: ['include', Validators.required],
    query: ['', Validators.compose([Validators.required])],
  });

  constructor(private formBuilder: FormBuilder) {}

  handleSubmit() {
    if (this.feedForm.valid) {
      this.submitRequest.emit(this.feedForm.value as any);
    }
  }
}
