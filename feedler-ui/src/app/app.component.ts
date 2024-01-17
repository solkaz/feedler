import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreateFeedFormComponent } from './create-feed-form/create-feed-form.component';
import { SubmitRequest } from './types';
import { ApiClientService } from './api-client.service';
import { FeedGeneratedViewComponent } from './feed-generated-view/feed-generated-view.component';

type View = 'form' | 'success';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, CreateFeedFormComponent, FeedGeneratedViewComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'feedler-ui';
  feedId: string | undefined;
  view: View = 'form';

  constructor(private apiClient: ApiClientService) {}

  handleSubmitRequest(submitRequest: SubmitRequest) {
    this.apiClient.createFeed(submitRequest).subscribe((feedId) => {
      console.log({ feedId });

      this.view = 'success';
      this.feedId = feedId;
    });
  }

  handleResetPage() {
    this.view = 'form';
  }
}
