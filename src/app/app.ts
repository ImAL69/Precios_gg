import { ChangeDetectionStrategy, Component, inject, OnInit, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './services/api.service';
import { SteamService } from './services/steam.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class App implements OnInit {
  private apiService = inject(ApiService);
  private steamService = inject(SteamService);

  protected readonly title = signal('Verificador de Precios');
  protected readonly message = signal<string>('');
  protected readonly juegos = signal<any[]>([]);
  protected readonly steamGames = signal<any[]>([]);
  protected readonly busqueda = signal<string>('');
  protected readonly loadingSteam = signal<boolean>(false);

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
    const query = this.busqueda();
    this.apiService.getJuegos(query).subscribe({
      next: (data) => this.juegos.set(data),
      error: (err) => console.error('Error al cargar juegos:', err)
    });

    if (query.length > 2) {
      this.buscarEnSteam(query);
    } else {
      this.steamGames.set([]);
    }
  }

  protected buscarEnSteam(term: string): void {
    this.loadingSteam.set(true);
    this.steamService.searchGames(term).subscribe({
      next: (data) => {
        this.steamGames.set(data.items || []);
        this.loadingSteam.set(false);
      },
      error: (err) => {
        console.error('Error al buscar en Steam:', err);
        this.loadingSteam.set(false);
      }
    });
  }

  protected onSearch(event: Event): void {
    const value = (event.target as HTMLInputElement).value;
    this.busqueda.set(value);
    this.cargarJuegos();
  }
}
