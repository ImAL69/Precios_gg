import { ChangeDetectionStrategy, Component, computed, inject, OnInit, signal } from '@angular/core';
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
  protected readonly epicGames = signal<any[]>([]);

  protected readonly allGames = computed(() => {
    const steam = this.steamGames().map(g => ({ ...g, platform: 'Steam' }));
    const epic = this.epicGames(); // Ya viene con platform: 'Epic Games'
    return [...steam, ...epic];
  });

  protected readonly categorias = signal<any[]>([]);
  protected readonly busqueda = signal<string>('');
  protected readonly categoriaSeleccionada = signal<string>('0');
  protected readonly loadingSteam = signal<boolean>(false);
  protected readonly expandedGames = signal<Set<number>>(new Set());

  ngOnInit(): void {
    this.cargarCategorias();
    this.cargarJuegos();
  }

  protected cargarCategorias(): void {
    this.apiService.getCategorias().subscribe({
      next: (data) => this.categorias.set(data),
      error: (err) => console.error('Error al cargar categorías:', err)
    });
  }

  protected cargarJuegos(): void {
    const query = this.busqueda();
    const category = this.categoriaSeleccionada();

    this.buscarEnSteam(query, category);
  }

  protected buscarEnSteam(term: string, categoryId: string = '0'): void {
    this.loadingSteam.set(true);

    // Buscar en Steam
    this.steamService.searchGames(term, categoryId).subscribe({
      next: (data) => {
        this.steamGames.set(data.items || []);
        this.loadingSteam.set(false);
      },
      error: (err) => {
        console.error('Error al buscar en Steam:', err);
        this.loadingSteam.set(false);
      }
    });

    // Buscar en Epic si hay término (Epic no soporta categorías tan fácil con esta API)
    if (term && term.length >= 3) {
      this.steamService.searchEpicGames(term).subscribe({
        next: (data) => this.epicGames.set(data.items || []),
        error: (err) => console.error('Error al buscar en Epic:', err)
      });
    } else {
      this.epicGames.set([]);
    }
  }

  protected onSearch(event: Event): void {
    const value = (event.target as HTMLInputElement).value;
    this.busqueda.set(value);
    this.cargarJuegos();
  }

  protected onCategoriaChange(event: Event): void {
    const value = (event.target as HTMLSelectElement).value;
    this.categoriaSeleccionada.set(value);
    this.cargarJuegos();
  }

  protected toggleExpand(juegoId: number): void {
    this.expandedGames.update(set => {
      const newSet = new Set(set);
      if (newSet.has(juegoId)) {
        newSet.delete(juegoId);
      } else {
        newSet.add(juegoId);
      }
      return newSet;
    });
  }

  protected isExpanded(juegoId: number): boolean {
    return this.expandedGames().has(juegoId);
  }
}
