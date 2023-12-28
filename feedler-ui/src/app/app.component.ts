import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreateFeedFormComponent } from './create-feed-form/create-feed-form.component';
import { SubmitRequest } from './types';
import { ApiClientService } from './api-client.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, CreateFeedFormComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'feedler-ui';

  constructor(private apiClient: ApiClientService) {}

  handleSubmitRequest(submitRequest: SubmitRequest) {
    this.apiClient.createFeed(submitRequest).subscribe((feedId) => {
      console.log({ feedId });
    });
  }
}
