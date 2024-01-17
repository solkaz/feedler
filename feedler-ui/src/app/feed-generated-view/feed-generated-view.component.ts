import { CommonModule } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Input,
  Output,
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
  @Input({ required: true }) feedId!: string;
  @Output() resetPage = new EventEmitter();

  onResetPageClicked() {
    this.resetPage.emit();
  }
}
