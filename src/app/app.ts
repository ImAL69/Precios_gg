import { ChangeDetectionStrategy, Component, inject, OnInit, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './services/api.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class App implements OnInit {
  private apiService = inject(ApiService);
  protected readonly title = signal('gg');
  protected readonly message = signal<string>('');

  ngOnInit(): void {
    this.apiService.getHello().subscribe({
      next: (data) => this.message.set(data.message),
      error: (err) => {
        console.error('Error al conectar con Django:', err);
        this.message.set('No se pudo conectar con el backend');
      }
    });
  }
}
