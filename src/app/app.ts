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

  protected readonly title = signal('Verificador de Precios');
  protected readonly message = signal<string>('');
  protected readonly juegos = signal<any[]>([]);
  protected readonly busqueda = signal<string>('');

  ngOnInit(): void {
    this.apiService.getHello().subscribe({
      next: (data) => this.message.set(data.message),
      error: (err) => {
        console.error('Error al conectar con Django:', err);
        this.message.set('No se pudo conectar con el backend');
      }
    });

    this.cargarJuegos();
  }

  protected cargarJuegos(): void {
    this.apiService.getJuegos(this.busqueda()).subscribe({
      next: (data) => this.juegos.set(data),
      error: (err) => console.error('Error al cargar juegos:', err)
    });
  }

  protected onSearch(event: Event): void {
    const value = (event.target as HTMLInputElement).value;
    this.busqueda.set(value);
    this.cargarJuegos();
  }
}
