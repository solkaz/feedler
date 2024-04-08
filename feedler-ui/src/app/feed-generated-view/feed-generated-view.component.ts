import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  input,
  output,
} from '@angular/core';

@Component({
  selector: 'app-feed-generated-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './feed-generated-view.component.html',
  styleUrl: './feed-generated-view.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FeedGeneratedViewComponent {
  feedId = input.required<string>();
  resetPage = output();

  onResetPageClicked() {
    this.resetPage.emit();
  }
}
